import sqlite3
import json
import pandas as pd

def query_database(sql_query, db_path="northwind-SQLite3/dist/northwind.db"):
    """
    Execute a SQL query on the Northwind database.
    
    Args:
        sql_query (str): The SQL query to execute
        db_path (str): Path to the northwind.db file
    
    Returns:
        dict: Query results with columns and data
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description] if cursor.description else []
        return {"columns": columns, "data": results}
    finally:
        conn.close()

def get_database_schema(db_path):
    """
    Extract table and column information from a SQLite database.
    
    Args:
        db_path (str): Path to the SQLite database file
    
    Returns:
        str: JSON string containing schema information optimized for LLM consumption
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'sqlite_sequence'")
        tables = cursor.fetchall()
        
        schema = {}
        
        for table in tables:
            table_name = table[0]
            
            # Get column information for each table
            cursor.execute(f"PRAGMA table_info([{table_name}])")
            columns = cursor.fetchall()
            
            schema[table_name] = {
                "columns": [
                    {
                        "name": col[1],
                        "type": col[2]
                    }
                    for col in columns
                ]
            }
        
        return json.dumps(schema, indent=2)
    
    finally:
        conn.close()

def export_results_to_csv(results, filename=None):
    """
    Export query results to CSV format.
    
    Args:
        results (dict): Query results with 'columns' and 'data' keys
        filename (str, optional): If provided, saves to file. Otherwise returns CSV string.
    
    Returns:
        str: CSV content as string, or file path if saved
    """
    if not results.get('data'):
        return "No data to export"
    
    df = pd.DataFrame(results['data'], columns=results['columns'])
    
    if filename:
        df.to_csv(filename, index=False)
        return filename
    else:
        return df.to_csv(index=False)

if __name__ == "__main__":

    """unittest for query_northwind"""
    sql_query = "SELECT * FROM Customers;"
    results = query_database(sql_query)
    print(results)
    
    """unittest for get_database_schema"""
    schema = get_database_schema("northwind-SQLite3/dist/northwind.db")
    print(schema)

