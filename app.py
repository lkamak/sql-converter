from flask import Flask, request, jsonify, render_template, send_file
import tempfile
import os

from sql_converter import SQL_Converter
from utils import query_database, export_results_to_csv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert_to_sql", methods=["POST"])
def convert_to_sql():

    nl_query = request.form["nl_query"]
    
    sql_converter = SQL_Converter()
    sql_query = sql_converter.convert_to_sql(nl_query)
    
    if request.is_json:
        return jsonify({"sql_query": sql_query})
    else:
        return render_template("index.html", sql_query=sql_query)
    
# Let's add a route that allows us to run the generated SQL query and display the results. Let's make sure that the output on the frontend is formatted in a nice way.
@app.route("/run_query", methods=["POST"])
def run_query():
    sql_query = request.form["sql_query"]
    
    results = query_database(sql_query)
    
    if request.is_json:
        return jsonify({"results": results})
    else:
        return render_template("index.html", results=results, sql_query=sql_query)

@app.route("/export_csv", methods=["POST"])
def export_csv():
    sql_query = request.form["sql_query"]
    
    results = query_database(sql_query)
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    csv_content = export_results_to_csv(results)
    temp_file.write(csv_content)
    temp_file.close()
    
    return send_file(temp_file.name, as_attachment=True, download_name='query_results.csv')

if __name__ == "__main__":
    app.run(debug=True)
