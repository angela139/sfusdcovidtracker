import requests
from bs4 import BeautifulSoup

URL = "https://www.sfusd.edu/covid-19-response-updates-and-resources/health-and-safety-guidelines/when-someone-gets-sick"
page = requests.get(URL)
soup = BeautifulSoup(page.text, 'html.parser')
overall_reported = soup.find_all("table")[1]
headers = []
header_search = overall_reported.find_all("th")
for header in header_search:
    headers.append(header.text)

print(headers)

table_data = []

for items in overall_reported.find_all("tr"):
    row = {}
    for td, th in zip(items.find_all("td"), headers):
        row[th] = td.text.replace('\n', '').strip()
    table_data.append(row)

print(table_data)