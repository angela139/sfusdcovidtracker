from flask import Flask
from flask import render_template
import pandas as pd
import csv

dict_list = []

app = Flask(__name__)


@app.route('/')
def index():
    with open('SFUSD_Covid_Cases.csv') as csv_file:
        data = csv.reader(csv_file)
        reverse_data = list(reversed(list(data)))

    count = len(list(reverse_data))
    if len(dict_list) > 0:
        pass
    else:
        for row in range(count):
            if row != (count - 1):
                dict_list.append({
                    "time": reverse_data[row][0],
                    "staff": reverse_data[row][1],
                    "student": reverse_data[row][2],
                    "color": reverse_data[row][3],
                    "total": reverse_data[row][4]
                })
            else:
                print("Last row")

    return render_template("index.html", dict_list=dict_list)


if __name__ == "__main__":
    app.run()
