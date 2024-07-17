import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_imdb_top_movies():
    url = 'https://www.imdb.com/chart/top/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Select rows from the table
    rows = soup.select('table.chart.full-width tr')
    
    # Debugging: Print the number of rows and a sample row
    print(f"Number of rows found: {len(rows)}")
    if len(rows) > 1:
        print(f"First row content: {rows[0]}")
    
    movies = []

    # Ensure there are enough rows before proceeding
    if len(rows) < 2:
        print("No data rows found.")
        return pd.DataFrame(movies)  # Return an empty DataFrame
    
    for row in rows[1:]:  # Skip the header row
        title_column = row.find('td', class_='titleColumn')
        rating_column = row.find('td', class_='imdbRating')

        # Ensure the columns exist before proceeding
        if not title_column or not rating_column:
            print("Missing title or rating column in a row.")
            continue
        
        title = title_column.a.text
        year = title_column.span.text.strip('()')
        rating = rating_column.strong.text
        link = 'https://www.imdb.com' + title_column.a['href']
        
        movie_page = requests.get(link)
        movie_soup = BeautifulSoup(movie_page.text, 'html.parser')
        
        genres = [genre.text for genre in movie_soup.find_all('span', class_='genre')]
        director = movie_soup.find('span', class_='credit_summary_item').a.text
        cast_list = movie_soup.select('table.cast_list tr')[1:6]
        cast = [actor.find('a').text.strip() for actor in cast_list]
        
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
else:
    print("df is not a DataFrame")
