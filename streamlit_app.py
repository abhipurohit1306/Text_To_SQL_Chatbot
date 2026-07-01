import streamlit as st
import requests


st.title("Text-to-SQL Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

        if message["role"] == "assistant":

            if "query" in message:
                with st.expander("Generated SQL"):
                    st.code(message["query"], language="sql")

            if "result" in message:
                with st.expander("Database Result"):
                    st.write(message["result"])




question = st.chat_input("Ask a database question")
if question:
    st.chat_message("user").write(question)

    st.session_state.messages.append(
    {
        "role": "user",
        "content": question
    }
)

    try:

        with st.spinner("Generating SQL and querying database..."):
            api_response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={
                    "question": question
                },
                timeout=30
            )

            api_response.raise_for_status()

            data = api_response.json()

    except requests.exceptions.Timeout:
        st.error("⏳ Request timed out. Please try again.")
        st.stop()

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Unable to connect to the backend server.")
        st.stop()

    except requests.exceptions.HTTPError:
        st.error("⚠️ Backend returned an error.")
        st.stop()

    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        st.stop()
        
    st.chat_message("assistant").write(data["answer"])

    with st.expander("Generated SQL"):
        st.code(data["query"], language="sql")

    with st.expander("Database Result"):
        st.write(data["result"])

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": data["answer"],
            "query": data["query"],
            "result": data["result"]
        }
    )