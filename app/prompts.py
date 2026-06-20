from langchain_core.prompts import ChatPromptTemplate

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

# SQL REPAIR PROMPT

repair_prompt = ChatPromptTemplate.from_template(
    """
    You are an expert MySQL developer.

    The SQL query below failed validation.

    Database Schema:
    {schema}

    User Question:
    {question}

    Invalid SQL:
    {query}

    Validation Error:
    {error}

    Fix the SQL query.

    Rules:
    1. Return ONLY SQL.
    2. No markdown.
    3. No explanations.
    4. No code fences.
    5. Single line only.

    Correct SQL:
    """
)


#chat history prompt

rewrite_prompt = ChatPromptTemplate.from_template(
    """
    You are a conversation assistant.

    Chat History:
    {chat_history}

    Current Question:
    {question}

    Rewrite the current question into a complete standalone question.

    Return ONLY the rewritten question.
    """
)
