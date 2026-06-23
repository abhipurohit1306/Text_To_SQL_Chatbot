from langchain_community.utilities import SQLDatabase
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

def get_db():
    return SQLDatabase.from_uri(
        mysql_uri,
        sample_rows_in_table_info=2
    )


#get the schema of database

def get_schema(db):
    schema = db.get_table_info()
    return schema


def get_schema_metadata():
    db = get_db()
    schema_metadata = {}
    for table_name, table in db._metadata.tables.items():
        schema_metadata[table_name] = [
            column.name
            for column in table.columns
        ]
    return schema_metadata


def run_query(query):
    db = get_db()
    return db.run(query)
