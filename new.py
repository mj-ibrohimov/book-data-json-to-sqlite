import re
import json
import sqlite3

with open("task1_d.json", "r", encoding="utf-8") as f:
    raw = f.read()

# ruby syntax to json
fixed = re.sub(r':(\w+)\s*=>', r'"\1":', raw)

# remove any commas after the last item of objects/arrays
# fruits = [
#   'apples',
#   'banana', // Trailing comma
# ];
fixed = re.sub(r',\s*}', '}', fixed)
fixed = re.sub(r',\s*]', ']', fixed)

data = json.loads(fixed)

print(f"Loaded {len(data)} books.")

conn = sqlite3.connect("books.db")
c = conn.cursor()

# Create main books table
c.execute("""
CREATE TABLE IF NOT EXISTS books (
    id TEXT PRIMARY KEY,
    title TEXT,
    author TEXT,
    genre TEXT,
    publisher TEXT,
    year INTEGER,
    price REAL,
    currency TEXT
)
""")

for book in data:
    price_str = str(book.get("price", "0"))
    if price_str.startswith("$"):
        currency = "USD"
        price = float(price_str.replace("$", ""))
    elif price_str.startswith("€"):
        currency = "EUR"
        price = float(price_str.replace("€", ""))
    else:
        currency = "USD"
        price = float(price_str)
    
    #quoting confusion, 
    c.execute("""
    INSERT OR REPLACE INTO books (id, title, author, genre, publisher, year, price, currency)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
    """, (str(book.get("id")), book.get("title"), book.get("author"),
          book.get("genre"), book.get("publisher"),
          book.get("year"), price, currency))


conn.commit()
print("Inserted all books.")

c.execute("DROP TABLE IF EXISTS summary")
c.execute("""
CREATE TABLE summary AS
SELECT
    year AS publication_year,
    COUNT(*) AS book_count,
    ROUND(AVG(
        CASE WHEN currency='EUR' THEN price*1.2
             ELSE price
        END
    ), 2) AS average_price
FROM books
GROUP BY year
ORDER BY year
""")
conn.commit()

# Save summary table as plain text
with open("summary_output.txt", "w", encoding="utf-8") as f:
    f.write("publication_year | book_count | average_price\n")
    f.write("---------------------------------------------\n")
    for row in c.execute("SELECT * FROM summary"):
        line = f"{row[0]} | {row[1]} | {row[2]}\n"
        f.write(line)

print("\nSaved summary table to summary_output.txt")

print("\nBooks table row count:")
c.execute("SELECT COUNT(*) FROM books")
print(c.fetchone()[0])

print("\nSummary table:")
for row in c.execute("SELECT * FROM summary"):
    print(row)

conn.close()
print("\nDone. Database saved as books.db")


#sqlite integer type is 8 byte but ID in .json file is larger and overflow error happened that's why 
# I used text method since it has no limit

