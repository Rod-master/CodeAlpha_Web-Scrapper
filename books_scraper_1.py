import requests
from bs4 import BeautifulSoup
import csv

# Configuration
BASE_URL = "http://books.toscrape.com/"
CATALOGUE_URL = BASE_URL + "catalogue/page-{}.html"
MAX_PAGES = 3
OUTPUT_FILE = "books_data.csv"

# Rating word-to-number mapping
RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}

def fetch_page(url):
    """Send HTTP GET request and return response if successful."""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Failed to fetch {url} (status {response.status_code})")
        return None
    return response

def parse_books(soup):
    """Extract book data from a BeautifulSoup page object."""
    books = []
    articles = soup.find_all("article", class_="product_pod")

    for article in articles:
        try:
            # Extract title from <h3> > <a title="...">
            h3_tag = article.find("h3")
            a_tag = h3_tag.find("a") if h3_tag else None
            title = a_tag["title"].strip() if a_tag else "N/A"

            # Extract price
            price_tag = article.find("p", class_="price_color")
            price = price_tag.text.strip() if price_tag else "N/A"

            # Extract star rating from class name (e.g. "star-rating Three")
            rating_tag = article.find("p", class_="star-rating")
            rating_word = rating_tag["class"][1] if rating_tag else "Zero"
            rating = RATING_MAP.get(rating_word, 0)

            # Extract availability and clean whitespace
            avail_tag = article.find("p", class_="instock availability")
            availability = " ".join(avail_tag.text.split()) if avail_tag else "N/A"

            # Build absolute product link
            relative_href = a_tag["href"] if a_tag else ""
            # Remove leading "../" prefixes to normalize path
            clean_href = relative_href.replace("../", "")
            link = BASE_URL + "catalogue/" + clean_href

            books.append({
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability,
                "link": link
            })

        except Exception as e:
            print(f"Warning: Skipped a book due to error: {e}")
            continue

    return books

def save_to_csv(books, filename):
    """Save list of book dicts to a CSV file."""
    fieldnames = ["title", "price", "rating", "availability", "link"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)
    print(f"\nData saved to '{filename}'")

def main():
    all_books = []

    # Scrape pages 1 through MAX_PAGES
    for page_num in range(1, MAX_PAGES + 1):
        url = CATALOGUE_URL.format(page_num)
        print(f"Scraping page {page_num}: {url}")

        response = fetch_page(url)
        if response is None:
            print("Stopping due to fetch error.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        books = parse_books(soup)
        all_books.extend(books)
        print(f"  Found {len(books)} books on page {page_num}")

    # Save all scraped data to CSV
    if all_books:
        save_to_csv(all_books, OUTPUT_FILE)

    # Print first 5 records
    print("\n--- First 5 Books ---")
    for i, book in enumerate(all_books[:5], start=1):
        print(f"\n[{i}] {book['title']}")
        print(f"    Price       : {book['price']}")
        print(f"    Rating      : {book['rating']}/5")
        print(f"    Availability: {book['availability']}")
        print(f"    Link        : {book['link']}")

    print(f"\nTotal books scraped: {len(all_books)}")

if __name__ == "__main__":
    main()
