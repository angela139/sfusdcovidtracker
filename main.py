import requests
from bs4 import BeautifulSoup
import datetime
import csv

URL = "https://www.sfusd.edu/covid-19-response-updates-and-resources/health-and-safety-guidelines/when-someone-gets-sick/covid-19-testing-dashboard"
page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')
overall_reported = soup.find_all("table")[0]

date_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
table_data = [str(date_updated)]

for rows in overall_reported.find_all("tr")[1:]:
    num = rows.find_all("td")
    table_data.append(num[1].get_text())

positivity_rate = "{:.3%}".format(int(table_data[4]) / 62800)
table_data.append(positivity_rate)
print(table_data)


with open("SFUSD_Covid_Cases.csv", 'a', newline='') as obj:
    csv_writer = csv.writer(obj)
    csv_writer.writerow(table_data)



