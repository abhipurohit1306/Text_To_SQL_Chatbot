import json
from datetime import datetime

def log_query(question, query, validation_status, answer, execution_time):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "query": query,
        "validation_status": validation_status,
        "answer": answer,
        "execution_time":execution_time
    }

    with open("query_logs.jsonl", "a") as f:
        f.write(
            json.dumps(log_entry)
            + "\n"
        )