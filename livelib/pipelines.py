import sqlite3
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LivelibPipeline:
    def process_item(self, item, spider):

        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS books
                        (id INTEGER PRIMARY KEY,
                          title text,
                          author text,
                          year integer,
                          rating real,
                          img text,
                          link text)
                        """)
        books = list(item.values())
        cursor.execute(f"SELECT * FROM books WHERE title = '{books[0]}'")
        select = cursor.fetchone()
        if select is not None:
            cursor.execute(f"UPDATE books SET rating='{books[3]}'")
            conn.commit()
        else:
            cursor.executemany(f"INSERT INTO books(title, author, year, rating, img, link)"
                               f"VALUES (?,?,?,?,?,?)", (books,))
            conn.commit()
