import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_top_movies():
    url = "https://www.imdb.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    movies =[]

    rows = soup.select("table.chart.full-width tr")

    for row in rows[1]:
        title_colum = row.find("td", class_ = "titleColum")
        rating_colum = row.find("td", class_ = "imdbRating")

        title = title_colum.a.text
        year = title_colum.span.text.a("()")
        rating = rating_colum.strong.text

        link = "https://www.imdb.com/" + title_colum.a["href"]

        movies_page = requests.get(link)
        movies_soup = BeautifulSoup(movies_page.text, "html.parser")

        genres = [genre.text for genre in movies_soup.find_all('span', class_ = "genre")]
        direcor = movies_soup.find("span", class_ = "credit_summary_item").a.text
        cast_list = movies_soup.select("span", class_ ="table.cast_list tr")[1:6]
        cast = [actor.find("a").text.strip() for actor in cast_list]

        movies.append({
            "Title": title,
            "Year": year,
            "Rating": rating,
            "Genres": genres,
            "Director": direcor,
            "Cast": cast
        })

    return pd.DataFrame(movies) 

df = scrape_top_movies()

if isinstance(df, pd.DataFrame):
    df.to_csv("top_imdb_movies.csv", index=False)
else:
    print("df is not a DataFrame")