import requests
from bs4 import BeautifulSoup
import datetime
import csv
import re

URL = "https://www.sfusd.edu/covid-19-response-updates-and-resources/health-and-safety-guidelines/when-someone-gets-sick/covid-19-testing-dashboard"
page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')
overall_reported = soup.find_all("table")[0]
dict_list = []

today_date = datetime.datetime.now().strftime("%Y-%m-%d")

web_date = soup.find_all("em")[0].get_text()
date_list = web_date[14:].replace("@", "").replace(",", "").split()
month = datetime.datetime.strptime(date_list[0], '%B').month
if int(date_list[1]) < 10:
    date_for_compare = date_list[2] + "-" + "0" + str(month) + "-0" + date_list[1]
    formatted_date = date_list[2] + "-" + "0" + str(month) + "-0" + date_list[1] \
                     + " " + date_list[3]
else:
    date_for_compare = date_list[2] + "-" + "0" + str(month) + "-" + date_list[1]
    formatted_date = date_list[2] + "-" + "0" + str(month) + "-" + date_list[1] \
                     + " " + date_list[3]

table_data = [formatted_date]

for rows in overall_reported.find_all("tr")[1:]:
    num = rows.find_all("td")
    case_num = re.sub("[^0-9]", "", num[1].get_text())
    table_data.append(case_num)

if today_date == date_for_compare:
    with open("SFUSD_Covid_Cases.csv", 'a') as obj:
        csv_writer = csv.writer(obj)
        csv_writer.writerow(table_data)
    print("Data updated")
else:
    print("Different. Data not updated yet for today.")
