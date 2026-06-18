from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os


load_dotenv()

#connecting my sql database

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
username = os.getenv("DB_USER")
password = quote_plus(os.getenv("DB_PASSWORD"))
database_schema = os.getenv("DB_NAME")
mysql_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_schema}"

db = SQLDatabase.from_uri(mysql_uri,sample_rows_in_table_info = 2)




#get the schema of database

def get_schema(db):
    schema = db.get_table_info()
    return schema


def get_schema_metadata():
    schema_metadata = {}
    for table_name, table in db._metadata.tables.items():
        schema_metadata[table_name] = [
            column.name
            for column in table.columns
        ]
    return schema_metadata



def validate_tables(query):
    schema_metadata = get_schema_metadata()
    valid_tables = set(schema_metadata.keys())
    query_lower = query.lower()
    detected_tables = []

    for table in valid_tables:
        if table.lower() in query_lower:
            detected_tables.append(table)
    if not detected_tables:
        return {
            "valid": False,
            "message": "No valid table found in query."
        }
    return {
        "valid": True,
        "tables": detected_tables
    }


def validate_columns(query):
    schema_metadata = get_schema_metadata()
    query_lower = query.lower()
    if "select" not in query_lower or "from" not in query_lower:
        return {
            "valid": False,
            "message": "Unable to parse query."
        }
    select_part = query.split("FROM")[0]
    columns = (
        select_part
        .replace("SELECT", "")
        .split(",")
    )
    columns = [
        column.strip()
        for column in columns
    ]
    for table, table_columns in schema_metadata.items():
        if table.lower() in query_lower:
            invalid_columns = []
            for column in columns:

                column = column.strip()

                if column == "*":
                    continue

                # Skip SQL functions
                if "(" in column or ")" in column:
                    continue

                if column not in table_columns:
                    invalid_columns.append(column)
            if invalid_columns:
                return {
                    "valid": False,
                    "message": f"Invalid columns: {invalid_columns}"
                }
    return {
        "valid": True
    }


llm = ChatGoogleGenerativeAI(
    model = "models/gemini-3.1-flash-lite",
    api_key = os.getenv("GOOGLE_API_KEY")
)



def validate_sql(query):
    """
    Validate generated SQL before execution.
    """

    if not query or not query.strip():
        return {
            "valid": False,
            "message": "Empty query generated.",
            "query": query
        }

    query = query.strip().rstrip(";")

    # Allow only SELECT queries
    if not query.upper().startswith("SELECT"):
        return {
            "valid": False,
            "message": "Only SELECT statements are allowed.",
            "query": query
        }

    # Block dangerous keywords
    dangerous_keywords = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "REPLACE"
    ]

    query_upper = query.upper()

    for keyword in dangerous_keywords:
        if keyword in query_upper:
            return {
                "valid": False,
                "message": f"Dangerous SQL operation detected: {keyword}",
                "query": query
            }
        
    # TABLE VALIDATION

    table_validation = validate_tables(query)
    if not table_validation["valid"]:
        return table_validation

    # COLUMN VALIDATION

    column_validation = validate_columns(query)
    if not column_validation["valid"]:
        return column_validation


    return {
        "valid": True,
        "message": "Query is valid"
    }

    
    





#create Prompt tremplate - SQL GENERATION PROMPT

prompt = ChatPromptTemplate.from_template(
    """
    You are an expert MySQL developer.

    Given the database schema below, generate a valid MySQL query.

    Rules:
    1. Return ONLY the SQL query.
    2. No markdown.
    3. No explanations.
    4. No code fences.
    5. Output must be a single line.

    Schema:
    {schema}

    Question:
    {question}

    SQL Query:
    """
)

#create the sql query chain using the LLM and prompt template

sql_chain = (
    RunnablePassthrough.assign(
        schema=lambda _: get_schema(db)
    )
    | prompt
    | llm
    | StrOutputParser()
)


def run_query(query):
    return db.run(query)


#answer prompt
answer_prompt = ChatPromptTemplate.from_template(
    """
    Based on the question, SQL query, and SQL result,
    provide a clear natural language answer.

    Question:
    {question}

    SQL Query:
    {query}

    SQL Result:
    {result}

    Answer:
    """
)


#ANSWER CHAIN

answer_chain = (
    answer_prompt
    | llm
    | StrOutputParser()
)

question = "what is the total income for Eire Corp"

query = sql_chain.invoke({
    "question": question
})


validation = validate_sql(query)

if not validation["valid"]:

    print(f"Validation Failed: {validation['message']}")

    print("\nGenerated SQL:")

    if "query" in validation:
        print(validation["query"])
    else:
        print(query)

else:

    result = run_query(query)

    answer = answer_chain.invoke({
        "question": question,
        "query": query,
        "result": result
    })

    print("\nGenerated SQL:")
    print(query)

    print("\nDatabase Result:")
    print(result)

    print("\nFinal Answer:")
    print(answer)

