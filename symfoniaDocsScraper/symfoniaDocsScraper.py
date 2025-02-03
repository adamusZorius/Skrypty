from bs4 import BeautifulSoup
import requests
import os
from pdfkit import from_url

url = 'https://pomoc.symfonia.pl/data/ambasic/-/100/data/html_spis.htm'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

allLinks = soup.findAll("img")

# Create a directory to save PDFs
if not os.path.exists('pdfs'):
    os.makedirs('pdfs')

for link in allLinks:
    print(link.next.get('href'))
    href = link.next.get('href')

    if href:  # Check if href is not None
        # Construct the full URL if it's a relative link
        full_url = requests.compat.urljoin(url, href)
        print(f"Processing: {full_url}")

        # Generate a filename for the PDF
        filename = href.split('/')[-1]  # Use the last part of the URL as the filename
        if not filename.endswith('.pdf'):
            filename += '.pdf'

        # Save the page as a PDF
        try:
            from_url(full_url, f'pdfs/{filename}')
            print(f"Saved: {filename}")
        except Exception as e:
            print(f"Failed to save {full_url}: {e}")

# for x in range(int(allPages) + 1):
#     urlPagination = 'https://www.fakturowo.pl/biura-rachunkowe?p=' + str(x)
        
#     responsePagination = requests.get(urlPagination)
#     soupPagination = BeautifulSoup(responsePagination.text, 'html.parser')
#     soupHrefs= soupPagination.findAll("tr")[1:]

#     for y in range(len(soupHrefs)):
#         allLinks.append(soupHrefs[y].a["href"])

# for href in allLinks:
#     url = "https://www.fakturowo.pl" + href
#     print(url)
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     dataRes = {}

#     try:
#         name = soup.find("td", string="Nazwa").next_sibling.text

#         dataRes["name"] = name
#     except:
#         dataRes["name"] = ""

#     try:
#         email = soup.find("td", string="Email").next_sibling.text

#         dataRes["email"] = email
#     except:
#         dataRes["email"] = ""

#     try:
#         phone = soup.find("td", string="Telefon").next_sibling.text

#         dataRes["phone"] = phone
#     except:
#         dataRes["phone"] = ""

#     try:
#         page = soup.find("td", string="Strona WWW").next_sibling.text

#         dataRes["page"] = page
#     except:
#         dataRes["page"] = ""

#     data.append(dataRes)

# with open('kontakt.csv', mode='w', newline='') as csv_file:
#     fieldnames = ['name', 'email', 'phone', 'page']
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     writer.writerow({"name": "Nazwa", "email": "Email", "phone": "Telefon", "page": "Strona WWW"})
#     for record in data:
#         writer.writerow(record)