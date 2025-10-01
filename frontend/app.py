import streamlit as st
import requests

# Set the backend API URL
API_URL = "http://localhost:8000"

st.title("HR Policy Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask a question about the HR policy..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Send request to the backend API
    with st.spinner("Thinking..."):
        try:
            response = requests.post(f"{API_URL}/query", json={"query": prompt})
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            
            answer = data.get("answer", "I couldn't find an answer.")
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the backend: {e}")