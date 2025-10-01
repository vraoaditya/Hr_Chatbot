import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

app = FastAPI()

# Load the FAISS index and retriever
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = vector_store.as_retriever()

# Initialize the Groq LLM
llm = ChatGroq(model_name="mixtral-8x7b-32768", api_key=groq_api_key)
#llm = ChatGroq(model_name="llama-3.1-8b-instant", api_key=groq_api_key)
# Define the prompt template
prompt = ChatPromptTemplate.from_template(
    """
    You are an AI assistant for a human resources department. 
    Answer the user's question based only on the provided context. 
    If the answer is not in the provided context, state that you cannot answer.
    
    Context: {context}
    
    Question: {input}
    """
)

# Create the RAG chain
document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_chatbot(request: QueryRequest):
    """
    Endpoint to process a user's query and return a RAG-based answer.
    """
    try:
        response = retrieval_chain.invoke({"input": request.query})
        answer = response['answer']
        source_docs = response['context']
        
        # Extract source information
        sources = [doc.metadata.get('source', 'Unknown source') for doc in source_docs]
        
        return {"answer": answer, "sources": sources}
    except Exception as e:
        return {"answer": f"An error occurred: {str(e)}", "sources": []}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
