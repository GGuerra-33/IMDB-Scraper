from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)


def scrape_imdb_top_movies():
    url = 'https://www.imdb.com/chart/top/'

    service = Service('path/to/chromedriver')
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    # Wait for the page to load fully
    driver.implicitly_wait(10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    rows = soup.select('table.chart.full-width tr')

    print(f"Number of rows found: {len(rows)}")  # Debugging statement

    if len(rows) <= 1:
        print("No data rows found.")
        return []

    movies = []

    for row in rows[1:]:
        title_column = row.find('td', class_='titleColumn')
        rating_column = row.find('td', class_='imdbRating')

        if not title_column or not rating_column:
            continue

        title = title_column.a.text
        year = title_column.span.text.strip('()')
        rating = rating_column.strong.text
        link = 'https://www.imdb.com' + title_column.a['href']

        print(f"Scraped movie: {title} ({year}), Rating: {rating}, Link: {link}")  # Debugging statement

        movies.append({
            'Title': title,
            'Year': year,
            'Rating': rating,
            'Link': link
        })

    return movies


@app.route('/api/imdb/top250', methods=['GET'])
def get_top_250_movies():
    movies = scrape_imdb_top_movies()
    return jsonify(movies)


if __name__ == '__main__':
    app.run(debug=True)
