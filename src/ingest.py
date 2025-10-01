from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS

def create_faiss_index(file_path: str):
    """
    Loads a PDF, splits it into chunks, creates embeddings, and builds a FAISS index.
    """
    print("Loading and splitting document...")
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    
    # Initialize embedding model
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("Creating and saving FAISS index...")
    # Create the FAISS index from the documents and embeddings
    vector_store = FAISS.from_documents(docs, embeddings)
    
    # Save the index to a local file
    vector_store.save_local("faiss_index")
    print("FAISS index created and saved successfully.")

if __name__ == "__main__":
    create_faiss_index("hr_policy.pdf")