from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape_movie_data():
    source = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

    r = requests.get(source)

    status_code = r.status_code

    if r.status_code == 200:
        print("Request succesful")

    if r.status_code != 200:
        print(f"Code failed with status code {status_code}")

    
    soup = BeautifulSoup(source, "html_parser")

    titles = soup.select()

