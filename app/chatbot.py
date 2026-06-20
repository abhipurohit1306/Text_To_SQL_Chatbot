

# print("\nStandalone Question:")
# print(standalone_question)







from app.memory import chat_history
from app.chains import (rewrite_chain, sql_chain, repair_chain, answer_chain)
from app.validator import validate_sql
from app.database import (db, get_schema, run_query)
from app.memory import chat_history

def process_question(question):
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
                "schema": get_schema(db),
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

    print("\nGenerated SQL:")
    print(query)

    print("\nDatabase Result:")
    print(result)

    print("\nFinal Answer:")
    return(answer)