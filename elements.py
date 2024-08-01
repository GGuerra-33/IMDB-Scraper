from bs4 import BeautifulSoup
import requests

url = "https://www.imdb.com/chart/moviemeter/"


user_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://google.com',
}

response = requests.get

response = requests.get(url, headers= user_headers)

html_content = response.content

statuscode = response.status_code

if response.status_code == 200:
    print("Connection succesful")

if response.status_code != 200:
    print(f"Code failed with status code {statuscode}")


soup = BeautifulSoup(html_content, "html.parser")
all_elements = soup.find_all()

elements_name = {element.name for element in all_elements}

for name in elements_name:
    print(name)
    