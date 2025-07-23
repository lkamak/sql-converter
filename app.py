from flask import Flask, request, jsonify, render_template, make_response

from sql_converter import SQL_Converter
from utils import query_database

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert_to_sql", methods=["POST"])
def convert_to_sql():

    nl_query = request.form["nl_query"]
    
    sql_converter = SQL_Converter()
    sql_query = sql_converter.convert_to_sql(nl_query)
    
    return render_template("index.html", sql_query=sql_query)
    
@app.route("/run_query", methods=["POST"])
def run_query():
    sql_query = request.form["sql_query"]
    
    results = query_database(sql_query)
    
    return render_template("index.html", results=results, sql_query=sql_query)

@app.route("/download_csv", methods=["POST"])
def down_load_csv():
    sql_query = request.form["sql_query"]
    
    results = query_database(sql_query)
    
    csv_data = "sep=,\n"
    for row in results["data"]:
        for value in row:
            csv_data += str(value) + ","
        csv_data = csv_data[:-1] + "\n"
    
    response = make_response(csv_data)
    response.headers["Content-Disposition"] = "attachment; filename=query_results.csv"
    response.headers["Content-type"] = "text/csv"
    
    return response

if __name__ == "__main__":
    app.run(debug=True)
