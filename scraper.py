import requests
from bs4 import BeautifulSoup
import datetime
import csv
import re
import schedule
import time

URL = "https://www.sfusd.edu/covid-19-response-updates-and-resources/health-and-safety-guidelines/when-someone-gets-sick/covid-19-testing-dashboard"


def job():
    # Getting new data for csv
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    overall_reported = soup.find_all("table")[0]
    dict_list = []

    # Date the website updated with new data
    web_date = soup.find_all("em")[0].get_text()

    # Array with month, day, time
    updated_date = web_date[14:].replace("@", "").replace(",", "")
    formatted_date = datetime.datetime.strptime(updated_date, '%B %d %Y  %H:%M').strftime('%m-%d-%Y %I:%M %p')

    # Array for table data, first index is date
    table_data = [formatted_date]

    # Adds data from table on website to array
    for rows in overall_reported.find_all("tr")[1:]:
        num = rows.find_all("td")
        case_num = re.sub("[^0-9]", "", num[1].get_text())
        table_data.append(case_num)

    # Opens csv to get previous data to calculate # of new cases
    with open("SFUSD_Covid_Cases.csv", "r") as csv_file:
        for line in csv_file:
            pass
        last_row = line
        last_row_array = last_row.split(',')

    # Number of new cases
    new_cases = int(table_data[4]) - int(last_row_array[4])

    # Add number of new cases to table_data array
    table_data.append(str(new_cases))

    # Putting new data into csv if data was updated
    if last_row_array[0] != formatted_date:
        with open("SFUSD_Covid_Cases.csv", 'a') as obj:
            csv_writer = csv.writer(obj)
            csv_writer.writerow(table_data)
        print("Data updated.")
    else:
        print("Data not updated yet for today.")


schedule.every().day.at('22:00').do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
