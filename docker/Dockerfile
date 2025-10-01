# Use a slim Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src src
COPY frontend frontend
COPY .env .
COPY hr_policy.pdf .

# Expose the ports for the API and Streamlit
EXPOSE 8000
EXPOSE 8501

# The CMD command is a bit tricky for running both. A common approach is to use a single script.
# For simplicity, we can have the Streamlit app call the backend running locally inside the same container.
# First, you need to run the ingestion script to create the FAISS index. You would do this outside of the container
# and then copy the resulting index. Or, for a self-contained image, you can run it during the build process.

# Build the FAISS index during the Docker build process
RUN python src/ingest.py

# Install large, complex packages first
RUN pip install --no-cache-dir faiss-cpu sentence-transformers

# Install the remaining packages
RUN pip install --no-cache-dir -r requirements.txt

# Start the API and the Streamlit app simultaneously using a shell script or a command line
CMD ["sh", "-c", "uvicorn src.api:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port=8501 --server.enableCORS=true --server.enableXsrfProtection=false"]