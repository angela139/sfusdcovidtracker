from flask import Flask
from flask import render_template
import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']
db_conn = psycopg2.connect(DATABASE_URL, sslmode='require')
db_cursor = db_conn.cursor()

app = Flask(__name__)


@app.route('/')
def index():
    # Arrays for holding case data
    case_dict_list = []
    case_graph_list = []
    school_dict_list = []

    # Resets list when page is refreshed since data is kept
    if len(case_dict_list) > 0:
        case_dict_list = []

    # Queries database for cases data
    db_cursor.execute(""" SELECT * FROM covid_cases_table ORDER BY "time" DESC """)
    cases_rows = db_cursor.fetchall()

    # Tuple for dictionary keys
    header_tuple = ("time", "staff", "student", "color", "total", "new_cases")

    # Adds each value in the tuple as a value in dictionary and puts it into an array
    for row in cases_rows:
        result = dict(zip(header_tuple, row))
        case_dict_list.append(result)

    for row in reversed(cases_rows):
        result = dict(zip(header_tuple, row))
        case_graph_list.append(result)

    db_cursor.execute(""" SELECT * FROM school_cases_table ORDER BY "time" DESC """)
    school_rows = db_cursor.fetchall()

    # Tuple for dictionary keys
    school_header = ("time", "pk5", "pk8", "middle", "high")

    # Adds each value in the tuple as a value in dictionary and puts it into an array
    for row in school_rows:
        result = dict(zip(school_header, row))
        school_dict_list.append(result)

    return render_template("index.html", case_dict_list=case_dict_list, case_graph_list=case_graph_list,
                           school_dict_list=school_dict_list)


if __name__ == "__main__":
    app.run()
