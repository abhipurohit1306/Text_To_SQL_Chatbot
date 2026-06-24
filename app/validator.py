from app.database import get_schema_metadata

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
                if "." in column:
                    column = column.split(".")[-1]

                if column not in table_columns:
                    invalid_columns.append(column)
            if invalid_columns:
                return {
                    "valid": False,
                    "message": f"Invalid columns: {invalid_columns}"
                }
            print("\nSCHEMA METADATA")
            print(schema_metadata)
    return {
        "valid": True
    }


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

    
    