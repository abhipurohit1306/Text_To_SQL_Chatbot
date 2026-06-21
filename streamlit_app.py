import streamlit as st
from app.chatbot import process_question

st.title("Text-to-SQL Chatbot")

question = st.chat_input("Ask a database question")
if question:
    st.chat_message("user: ").write(question)

    response = process_question(question)
    st.chat_message("assistant").write(response["answer"])

    with st.expander("Generated SQL"):
        st.code(response["query"], language="sql")

    with st.expander("Database Result"):
        st.write(response["result"])