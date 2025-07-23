# NL to SQL Project Plan

## Objective

The idea for this project is to build a system that can translate natural language queries into SQL queries. The system will be able to understand the intent of the user and generate the appropriate SQL query. The system will be able to handle complex queries and will be able to generate queries for multiple databases.

## Workflow

The system will be built using the following workflow:

1. User inputs a query into a simple text box in the frontend
2. The user inputs the database schema (Table names and column names)
3. The payload is sent to the backend and Langchain is used to call a foundational model with the full context (Claude for now) to generate the SQL query
4. The response from the model is then sent back to the frontend
5. The frontend displays the generated SQL query



