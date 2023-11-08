import csv
import os

from lxml import etree
import requests

# This URL comes from:
# https://www.six-group.com/en/products-services/financial-information/data-standards.html#scrollTo=currency-codes
url = "https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml"

r = requests.get(url)
tree = etree.fromstring(r.content)

data = {
    el.find("Ccy").text: el.find("CcyNm").text
    for el in tree.xpath("//CcyNtry")
    if el.find("Ccy") is not None
}

data = [
    {
        "code": k,
        "name": v,
    }
    for k, v in sorted(data.items())
]

os.makedirs("output", exist_ok=True)
with open(os.path.join("output", "currency_codes.csv"), 'w') as csv_f:
    csvwriter = csv.DictWriter(csv_f, fieldnames=data[0].keys())
    csvwriter.writeheader()
    for row in data:
        csvwriter.writerow(row)
