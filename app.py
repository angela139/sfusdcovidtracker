from flask import Flask
from flask import render_template
import csv

dict_list = []
graph_list = []

app = Flask(__name__)


@app.route('/')
def index():
    with open('SFUSD_Covid_Cases.csv') as csv_file:
        data = csv.reader(csv_file)
        graph_data = list(data)
        reverse_data = list(reversed(graph_data))

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
                    "total": reverse_data[row][4],
                    "new_cases": reverse_data[row][5]
                })
            if row != 0:
                graph_list.append({
                    "time": graph_data[row][0],
                    "staff": graph_data[row][1],
                    "student": graph_data[row][2],
                    "color": graph_data[row][3],
                    "total": graph_data[row][4],
                    "new_cases": graph_data[row][5]
                })
            else:
                print("Category row")
    csv_file.close()
    return render_template("index.html", dict_list=dict_list, graph_list=graph_list)


if __name__ == "__main__":
    app.run()
