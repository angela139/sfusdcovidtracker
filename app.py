from flask import Flask
from flask import render_template
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

t_host = "localhost"
t_port = "5432"
t_dbname = "sfusd_covid_cases"
t_user = os.getenv('USERNAME')
t_pw = os.getenv('PASSWORD')

dict_list = []
graph_list = []

db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname,
                           user=t_user, password=t_pw)
db_cursor = db_conn.cursor()

app = Flask(__name__)


@app.route('/')
def index():
    # Queries database for cases data

    db_cursor.execute(""" SELECT * FROM covid_cases_table ORDER BY "time" DESC """)
    cases_rows = db_cursor.fetchall()

    # Tuple for dictionary keys
    header_tuple = ("time", "staff", "student", "color", "total", "new_cases")

    # Adds each value in the tuple as a value in dictionary and puts it into an array
    for row in cases_rows:
        result = dict(zip(header_tuple, row))
        dict_list.append(result)

    for row in reversed(cases_rows):
        result = dict(zip(header_tuple, row))
        graph_list.append(result)

    return render_template("index.html", dict_list=dict_list, graph_list=graph_list)


if __name__ == "__main__":
    app.run()
