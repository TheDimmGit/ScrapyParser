import sqlite3
from datetime import datetime
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LivelibPipeline:
    def process_item(self, item, spider):

        conn = sqlite3.connect('books.db')      # DB creation
        cursor = conn.cursor()
        name = str(datetime.now().strftime("%Y-%m-%d %H:%M")).replace('-', '').replace(':', '')  # Table name in YMD format
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS '{name}'
                        (id INTEGER PRIMARY KEY,
                          title text,
                          author text,
                          year integer,
                          rating real,
                          img text,
                          link text)
                        """)        # Creating new table with date name for each script run
        books = list(item.values())     # List of all books(item variable is dict with every book parameter)
        cursor.executemany(f"INSERT INTO '{name}'(title, author, year, rating, img, link) "
                           f"VALUES (?,?,?,?,?,?)", (books,))       # Inserting all information into columns
        conn.commit()     # DB connection closed
        return item
