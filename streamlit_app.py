import streamlit as st
from app.chatbot import process_question


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

    response = process_question(question)
    st.chat_message("assistant").write(response["answer"])

    with st.expander("Generated SQL"):
        st.code(response["query"], language="sql")

    with st.expander("Database Result"):
        st.write(response["result"])

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response["answer"],
            "query": response["query"],
            "result": response["result"]
        }
    )