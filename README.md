# 📚 Books Scraper

A beginner-friendly Python web scraper that collects book data from [books.toscrape.com](http://books.toscrape.com) and saves it as a structured CSV file.

It scrapes the first 3 pages of the catalogue, extracting title, price, star rating, availability, and a direct product link for each book.

---

## 🛠 Technologies Used

- Python 3
- `requests` — for sending HTTP GET requests
- `beautifulsoup4` — for parsing HTML
- `csv` — built-in module for saving structured data

---

## 🚀 How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/books-scraper.git
   cd books-scraper
   ```

2. **Install dependencies**
   ```bash
   pip install requests beautifulsoup4
   ```

3. **Run the scraper**
   ```bash
   python books_scraper.py
   ```

4. **Output**
   - A file named `books_data.csv` will be created in the same directory
   - The first 5 scraped books will be printed to the terminal
   - Total book count will be displayed at the end

---

## 📄 Sample Output

**Terminal:**
```
Scraping page 1: http://books.toscrape.com/catalogue/page-1.html
  Found 20 books on page 1
...
Data saved to 'books_data.csv'

--- First 5 Books ---

[1] A Light in the Attic
    Price       : £51.77
    Rating      : 3/5
    Availability: In stock
    Link        : http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html
...
Total books scraped: 60
```

**CSV columns:** `title`, `price`, `rating`, `availability`, `link`

---

## 📁 Project Structure

```
books-scraper/
├── books_scraper.py   # Main scraping script
├── books_data.csv     # Sample output (auto-generated)
└── README.md          # This file
```
