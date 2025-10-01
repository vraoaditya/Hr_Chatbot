## RAG HR Chatbot

## Project Overview

This is a Retrieval-Augmented Generation (RAG) chatbot designed to answer employee questions based on a provided HR policy document. The application uses a RAG pipeline to retrieve relevant information from the document and generate accurate, context-aware responses.

**Core Features**

  * **Document Ingestion:** Processes a provided HR policy PDF, extracting and cleaning the text.
  * **Vector Search:** Creates a FAISS index from document embeddings for efficient and fast retrieval of relevant information.
  * **RAG Pipeline:** Combines a retriever with a Large Language Model (LLM) to generate grounded responses.
  * **Backend API:** A FastAPI server exposes a `/query` endpoint to handle user questions.
  * **Minimal Frontend:** A Streamlit web interface provides a simple chat UI for user interaction.
  * **Containerization:** The entire application is packaged in a Docker container for easy and consistent deployment across different environments.

## Technologies Used

  * **Python:** The core programming language for the entire application.
  * **LangChain:** Framework used to build the RAG pipeline.
  * **FAISS:** Library for efficient similarity search, used as the vector store.
  * **Sentence Transformers:** Model used to create embeddings from the text.
  * **Groq:** Provides the high-speed LLM for text generation.
  * **FastAPI:** The web framework for building the backend API.
  * **Streamlit:** The framework for the interactive web-based frontend.
  * **Docker:** Used for containerizing and deploying the application.

## Project Structure

```
rag_hr_chatbot/
├── .env
├── requirements.txt
├── hr_policy.pdf
├── src/
│   ├── ingest.py
│   ├── rag_pipeline.py
│   └── api.py
├── frontend/
│   └── app.py
├── docker/
│   └── Dockerfile
└── README.md
```

## Setup Instructions

### **Prerequisites**

  * **Docker Desktop:** Ensure you have Docker Desktop installed and running. You can verify this by running `docker run hello-world` in your terminal.
  * **Git:** Make sure Git is installed on your system.

### **1. Configure Your Environment**

1.  **Clone the Repository:** Clone this project to your local machine.

    ```bash
    git clone https://github.com/vraoaditya/Hr_Chatbot.git
    cd Hr_Chatbot
    ```

2.  **Set up API Key:** Obtain an API key from the Groq console. Create a `.env` file in the root of the project and add your key:

    ```ini
    GROQ_API_KEY="YOUR_API_KEY_HERE"
    ```

### **2. Build the Docker Image**

This command builds the Docker image for your application. It performs all the necessary steps, such as installing dependencies and building the FAISS index.

1.  Open your terminal and navigate to the project's root directory: `C:\rag_hr_chatbot`.
2.  Run the build command, specifying the location of the `Dockerfile`:
    ```bash
    docker build -t hr_chatbot_image . -f ./docker/Dockerfile
    ```

### **3. Run the Docker Container**

Once the image is built, you can run a container from it. This command starts both the FastAPI backend and the Streamlit frontend.

```bash
docker run -d -p 8501:8501 -p 8000:8000 --name hr_chatbot hr_chatbot_image
```

## Usage

1.  Open your web browser and go to `http://localhost:8501`.
2.  You will see the Streamlit chat interface. Type a question related to the HR policy document into the input box at the bottom.
3.  The chatbot will provide a response based on the document's content.

## Troubleshooting

  * **`ERR_CONNECTION_REFUSED`:** This error often means a local server is not running. Ensure your Docker container is running by using the `docker ps` command.
  * **`Docker is not recognized...`:** This means Docker is not installed or configured on your system. Please install Docker Desktop and restart your machine.
  * **`Failed to receive status: rpc error`:** This indicates a connection issue with the Docker daemon. A simple restart of Docker Desktop or your computer can often fix this.
