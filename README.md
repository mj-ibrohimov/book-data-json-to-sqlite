# Ruby JSON to SQLite Book Processor

This project converts a Ruby-style JSON file (`task1_d.json`) into valid JSON, loads the data into a SQLite database, normalizes currency values, and generates a summary analytics table.  
The script also exports the summary table as a plain text output file.

## 📘 Features

- Converts Ruby hash syntax (`:key => value`) into valid JSON
- Cleans trailing commas inside objects and arrays
- Loads book data into a SQLite database (`books.db`)
- Handles multi-currency price values ($ and €)
- Automatically converts EUR to USD (×1.2 rate) for analytics
- Creates a summary table with:
  - Publication year  
  - Book count  
  - Average price (USD-normalized)
- Saves summary results into `summary_output.txt`

## 📊 Example Summary Output

| publication_year | book_count | average_price |
|-----------------|------------|---------------|
| 1995            | 12         | 14.50         |
| 1996            | 8          | 16.10         |
| 1997            | 10         | 15.40         |
