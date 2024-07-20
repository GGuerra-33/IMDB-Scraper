from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_imdb_top_movies():
    # Set up Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service('path_to_chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    url = 'https://www.imdb.com/chart/top/'
    driver.get(url)
    
    # Get page source and close driver
    html = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    rows = soup.select('table.chart.full-width tr')
    
    movies = []

    if len(rows) < 2:
        print("No data rows found.")
        return pd.DataFrame(movies)
    
    for row in rows[1:]:
        title_column = row.find('td', class_='titleColumn')
        rating_column = row.find('td', class_='imdbRating')

        if not title_column or not rating_column:
            print("Missing title or rating column in a row.")
            continue
        
        title = title_column.a.text
        year = title_column.span.text.strip('()')
        rating = rating_column.strong.text
        link = 'https://www.imdb.com' + title_column.a['href']
        
        movie_page = requests.get(link)
        movie_soup = BeautifulSoup(movie_page.text, 'html.parser')
        
        genres = [genre.text.strip() for genre in movie_soup.find_all('span', class_='genre')]
        director = movie_soup.find('span', class_='credit_summary_item').a.text.strip()
        cast_list = movie_soup.select('table.cast_list tr')[1:6]
        cast = [actor.find('a').text.strip() for actor in cast_list if actor.find('a')]
        
        movies.append({
            'Title': title,
            'Year': year,
            'Rating': rating,
            'Genres': genres,
            'Director': director,
            'Cast': cast
        })
    
    return pd.DataFrame(movies)

# Scrape the data
df = scrape_imdb_top_movies()

# Check if df is a DataFrame
if isinstance(df, pd.DataFrame):
    # Save the DataFrame to a CSV file
    df.to_csv('imdb_top_movies.csv', index=False)
    print("Data successfully saved to imdb_top_movies.csv")
else:
    print("df is not a DataFrame")

