from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os


    
from app.chatbot import process_question

while True:
    question = input("\nAsk a question: ")

    if question.lower() in ["bye", "quit", "exit"]:
        print("\nGoodbye!")
        break

    answer = process_question(question)

    print(answer)



    


