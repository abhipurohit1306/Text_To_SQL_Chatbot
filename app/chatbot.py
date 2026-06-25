from app.memory import chat_history
from app.chains import (rewrite_chain, sql_chain, repair_chain, answer_chain)
from app.validator import validate_sql
from app.database import run_query
from app.memory import chat_history
from app.database import get_db, get_schema
from app.logger import log_query
import time

def process_question(question):
    start_time = time.perf_counter()
    standalone_question = rewrite_chain.invoke(
        {
            "chat_history": chat_history,
            "question": question
        }
    )
    query = sql_chain.invoke({
        "question": standalone_question
    })

    validation = validate_sql(query)

    if not validation["valid"]:

        print(f"\nValidation Failed: {validation['message']}")

        print("\nAttempting SQL Repair...")

        repaired_query = repair_chain.invoke(
            {
                "schema": get_schema(get_db()),
                "question": standalone_question,
                "query": query,
                "error": validation["message"]
            }
        )

        print("\nRepaired SQL:")
        print(repaired_query)

        repaired_validation = validate_sql(repaired_query)

        if repaired_validation["valid"]:

            print("\nRepair Successful!")

            query = repaired_query

        else:

            print("\nRepair Failed")

            print(repaired_validation["message"])

            exit()



    result = run_query(query)
    answer = answer_chain.invoke(
        {
            "question": standalone_question,
            "query": query,
            "result": result
        }
    )

    chat_history.append(
        {
            "question": question,
            "answer": answer
        }
    )

    end_time = time.perf_counter()
    execution_time = round(end_time - start_time, 3)
    
    log_query(
        question=question,
        query=query,
        validation_status = validation["message"],
        answer=answer,
        execution_time=execution_time
    )

    

    return {
        "query": query,
        "result": result,
        "answer": answer,
        "execution_time": execution_time
    }