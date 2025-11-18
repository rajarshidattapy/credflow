import streamlit as st
import httpx
import uuid
import os
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="CrediFlow Agent Command Center",
    page_icon="🤖",
    layout="wide"
)

# --- App Title ---
st.title("🤖 CrediFlow Agent Command Center")
st.caption("A live dashboard for the autonomous loan processing agent.")

# --- Backend API URL ---
# This points to our FastAPI backend.
# When running locally in Cloud Shell, "http://localhost:8080" is correct.
# When deployed, we will change this to the Cloud Run URL.
API_BASE_URL = os.environ.get("API_URL", "http://localhost:8080")
CHAT_ENDPOINT = f"{API_BASE_URL}/chat"

# --- Session State Management ---
# We need to store the chat history and session_id
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.last_trace = None # To store the agent's "thoughts"

# --- Main Layout (2 Columns) ---
col_chat, col_dashboard = st.columns([1, 1]) # 50% width for each

# --- Column 1: The Chat Interface ---
with col_chat:
    st.header("💬 Customer Chat")
    
    # Display existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input box at the bottom
    if prompt := st.chat_input("What would you like to say?"):
        
        # 1. Add user's message to chat history and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Call the FastAPI backend
        try:
            with st.spinner("Agent is thinking..."):
                payload = {
                    "session_id": st.session_state.session_id,
                    "message": prompt
                }
                
                # Use httpx for async-compatible POST request
                with httpx.Client(timeout=120.0) as client: # 120 sec timeout for agent
                    response = client.post(CHAT_ENDPOINT, json=payload)
                
                response.raise_for_status() # Raise an exception for 4xx/5xx errors
                
                # 3. Process the successful response
                data = response.json()
                agent_response = data["agent_response"]
                st.session_state.last_trace = data["trace"] # Save the trace
                
                # 4. Add agent's response to chat and display it
                st.session_state.messages.append({"role": "assistant", "content": agent_response})
                with st.chat_message("assistant"):
                    st.markdown(agent_response)

        except httpx.HTTPStatusError as e:
            st.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            st.session_state.last_trace = {"error": str(e.response.text)}
        except httpx.RequestError as e:
            st.error(f"Connection error: Could not reach API. Is it running? Error: {e}")
            st.session_state.last_trace = {"error": f"Connection Error: {e}"}
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            st.session_state.last_trace = {"error": str(e)}

        # Rerun to update the dashboard column
        st.rerun()

# --- Column 2: The Agent "Thought" Dashboard ---
with col_dashboard:
    st.header("🧠 Agent Live Trace")
    
    if st.session_state.last_trace:
        st.info("Showing the most recent agent trace. This is the 'thought process' from the backend.")
        st.json(st.session_state.last_trace, expanded=True)
    else:
        st.info("The agent's thoughts and tool calls will appear here once the chat begins.")