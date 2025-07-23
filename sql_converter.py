from utils import query_database, get_database_schema
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class SQL_Converter:
    def __init__(self, db_path="northwind-SQLite3/dist/northwind.db"):
        self.db_path = db_path

        self.db_schema = get_database_schema(self.db_path)

        self.llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            api_key=os.getenv("ANTHROPIC_API_KEY"), 
            temperature=0
        )

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("human", "Schema:\n{schema}\n\nQuery: {nl_query}\n\nGenerate SQL:")
        ])

        self.llm_chain = self.prompt_template | self.llm | StrOutputParser()

    def _get_system_prompt(self) -> str:
        return """You are an expert SQL generator. Convert natural language queries to SQL based on the provided database schema.

Rules:
1. Generate ONLY the SQL query, no explanations or markdown formatting
2. Use proper SQL syntax and formatting
3. Be conservative - if the query is ambiguous, make reasonable assumptions
4. Use appropriate JOINs when querying multiple tables
5. Include proper WHERE clauses for filtering
6. Use aggregate functions (COUNT, SUM, AVG, etc.) when appropriate
7. Always end queries with a semicolon

Examples:

Schema: 
CREATE TABLE employees (id INT, name VARCHAR, department VARCHAR, salary INT);
CREATE TABLE departments (id INT, name VARCHAR, budget INT);

Natural Language: "Show me all employees in the engineering department"
SQL: SELECT * FROM employees WHERE department = 'engineering';

Natural Language: "What's the average salary by department?"
SQL: SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department;

Natural Language: "How many employees are in each department with their department budget?"
SQL: SELECT d.name, COUNT(e.id) as employee_count, d.budget 
     FROM departments d 
     LEFT JOIN employees e ON d.name = e.department 
     GROUP BY d.name, d.budget;
"""

    def convert_to_sql(self, nl_query: str) -> str:

        try:
            result = self.llm_chain.invoke({"schema": self.db_schema, "nl_query": nl_query})
        except Exception as e:
            print(f"Error in convert_to_sql: {e}")
            return "Error: " + str(e)
        
        return result

if __name__ == "__main__":

    """unittest for SQL_Converter"""

    sql_converter = SQL_Converter()
    nl_query = "What are the top 5 products with the largest average order size?"
    sql_query = sql_converter.convert_to_sql(nl_query)
    print(sql_query)

    """unittest for query_database"""
    result = query_database(sql_query)
    print(result)

    pass
