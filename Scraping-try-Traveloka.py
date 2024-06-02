from bs4 import BeautifulSoup
import requests

url = "https://www.traveloka.com/id-id"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

data = []
agains = soup.findAll('//*[@id="__next"]/div[1]/div[2]/div/div[2]/div')

for again in agains:
    nama = again.find('//*[@id="__next"]/div[1]/div[2]/div/div[2]/div/div/a[*]/div').text

    data.append(nama)

print(data)
