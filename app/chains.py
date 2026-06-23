from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
from app.database import get_db, get_schema
from app.prompts import (prompt,answer_prompt,repair_prompt,rewrite_prompt)

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "models/gemini-3.1-flash-lite",
    api_key = os.getenv("GOOGLE_API_KEY")
)


#create the sql query chain using the LLM and prompt template

sql_chain = (
    RunnablePassthrough.assign(
        schema=lambda _: get_schema(get_db())
    )
    | prompt
    | llm
    | StrOutputParser()
)

#ANSWER CHAIN

answer_chain = (
    answer_prompt
    | llm
    | StrOutputParser()
)

#repair chain

repair_chain = (
    repair_prompt
    | llm
    | StrOutputParser()
)

#rewrite chain
rewrite_chain = (
    rewrite_prompt
    | llm
    | StrOutputParser()
)