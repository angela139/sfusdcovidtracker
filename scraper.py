import requests
from bs4 import BeautifulSoup
import datetime
import re
import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']
URL = "https://www.sfusd.edu/covid-19-response-updates-and-resources/health-and-safety-guidelines/when-someone-gets-sick/covid-19-testing-dashboard"

db_conn = psycopg2.connect(DATABASE_URL, sslmode='require')
db_cursor = db_conn.cursor()


def job():
    # Getting new data for sql database
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    overall_reported = soup.find_all("table")[0]
    school_reported = soup.find_all("table")[2]

    # Date the website updated with new data
    web_date = soup.find_all("em")[0].get_text()

    # Array with month, day, time
    updated_date = web_date[14:].replace("@", "").replace(",", "")
    formatted_date = datetime.datetime.strptime(updated_date, '%B %d %Y  %H:%M').strftime('%m-%d-%Y %I:%M %p')

    # Array for overall cases table data, first index is date
    overall_table_data = [formatted_date]
    schools_table_data = [formatted_date]

    # Adds data from table on website to array
    for rows in overall_reported.find_all("tr")[1:]:
        num = rows.find_all("td")
        case_num = re.sub("[^0-9]", "", num[1].get_text())
        overall_table_data.append(case_num)

    for rows in school_reported.find_all("tr")[2:6]:
        num = rows.find_all("td")
        case_num = re.sub("[^0-9]", "", num[1].get_text())
        schools_table_data.append(case_num)

    # Queries previous day's data from sql database
    db_cursor.execute(""" SELECT total FROM covid_cases_table
    ORDER BY "time" DESC LIMIT 1 """)
    p_cases = db_cursor.fetchone()
    db_cursor.execute(""" SELECT time FROM covid_cases_table
    ORDER BY "time" DESC LIMIT 1 """)
    p_updated = db_cursor.fetchone()

    # Converts sql queries aka tuples to strings
    previous_cases = ''.join(p_cases)
    previous_updated = ''.join(p_updated)

    # Number of new cases
    new_cases = int(overall_table_data[4]) - int(previous_cases)

    # Add number of new cases to overall_table_data array
    overall_table_data.append(str(new_cases))

    # Adds new data if updated
    if previous_updated != formatted_date:
        covid_sql_query = """ INSERT INTO covid_cases_table(time, staff, student, 
        color, total, new) VALUES (%s,%s,%s,%s,%s,%s) """
        db_cursor.execute(covid_sql_query, overall_table_data)
        school_sql_query = """ INSERT INTO school_cases_table(time, pk5, pk8, middle, high) VALUES (%s,%s,%s,%s,%s)"""
        db_cursor.execute(school_sql_query, schools_table_data)
        db_conn.commit()
        db_cursor.close()
        db_conn.close()
    else:
        print("Data not updated yet for today.")