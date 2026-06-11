from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import create_sql_query_chain
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from urllib.parse import quote_plus



#connecting my sql database

host = 'localhost'
port = '3306'
username = 'root'
password = quote_plus("Akki@123")
database_schema = 'text_to_sql'

mysql_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_schema}"

db = SQLDatabase.from_uri(mysql_uri,sample_rows_in_table_info = 2)

print(db.get_table_info())