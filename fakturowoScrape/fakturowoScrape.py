from bs4 import BeautifulSoup
import requests
import csv

url = 'https://www.fakturowo.pl/biura-rachunkowe?p=0'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

soupPaginationNumber = soup.find("ul", class_="pagination-custom")
allPages = soupPaginationNumber.find_all("li")[-1].a["href"][-2:]

allLinks = []
data = []

for x in range(int(allPages) + 1):
    urlPagination = 'https://www.fakturowo.pl/biura-rachunkowe?p=' + str(x)

    responsePagination = requests.get(urlPagination)
    soupPagination = BeautifulSoup(responsePagination.text, 'html.parser')
    soupHrefs= soupPagination.findAll("tr")[1:]

    for y in range(len(soupHrefs)):
        allLinks.append(soupHrefs[y].a["href"])

for href in allLinks:
    url = "https://www.fakturowo.pl" + href
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    dataRes = {}

    try:
        name = soup.find("td", string="Nazwa").next_sibling.text

        dataRes["name"] = name
    except:
        dataRes["name"] = ""

    try:
        email = soup.find("td", string="Email").next_sibling.text

        dataRes["email"] = email
    except:
        dataRes["email"] = ""

    try:
        phone = soup.find("td", string="Telefon").next_sibling.text

        dataRes["phone"] = phone
    except:
        dataRes["phone"] = ""

    try:
        page = soup.find("td", string="Strona WWW").next_sibling.text

        dataRes["page"] = page
    except:
        dataRes["page"] = ""

    data.append(dataRes)

with open('kontakt.csv', mode='w', newline='') as csv_file:
    fieldnames = ['name', 'email', 'phone', 'page']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writerow({"name": "Nazwa", "email": "Email", "phone": "Telefon", "page": "Strona WWW"})
    for record in data:
        writer.writerow(record)