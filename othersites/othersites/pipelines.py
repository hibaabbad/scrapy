# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import mysql.connector

import re

class PricePipeline:

    def process_item(self, item, spider):
        # Remove commas and currency symbol from the 'price' attribute
        price_str = re.sub(r'[^\d.]', '', item['price'])
        
        # Convert the cleaned 'price' to a float
        try:
            item['price'] = float(price_str)
        except ValueError:
            # Handle the case where conversion fails (e.g., if 'price' is not a valid number)
            item['price'] = None  # You can set a default value or handle it accordingly

        # Rest of your processing logic...

        return item
        
class DuplicatesPipeline:

    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['name'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter['name'])
            return item
        
        
        
        
# pipelines.py


class MysqlDemoPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = '127.0.0.1',
            user = 'root',
            password = 'jiminssi&love10',
            database = 'jumia'
        )

          # Create cursor and laptops table if it doesn't exist
        with self.conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS laptops (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                price VARCHAR(255),
                url TEXT,
                photo TEXT,
                description TEXT,
                type VARCHAR(255),
                disque VARCHAR(255),
                ram VARCHAR(255),
                cpu VARCHAR(255),
                marque VARCHAR(255),
                ecran VARCHAR(255)
            )
            """)
        
    def process_item(self, item, spider):
        try:
            # Define insert statement for laptops table
            insert_query = """
                INSERT INTO laptops (name, price, url, photo, description, type, disque, ram, cpu, marque, ecran)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            

            # Execute insert statement
            with self.conn.cursor() as cur:
                cur.execute(insert_query, (
                    item['name'],
                    item['price'],
                    item['url'],
                    item.get('photo', None),
                    item.get('description', None),
                    item['type'],
                    item.get('disque', None),
                    item.get('ram', None),
                    item.get('cpu', None),
                    item['marque'],
                    item.get('ecran', None)
                ))

        except mysql.connector.Error as err:
            # Log the error and raise DropItem to skip the item
            spider.logger.error(f"MySQL Error: {err}")
            raise DropItem(f"MySQL Error: {err}")

        return item

    def close_spider(self, spider):
        # Commit changes to the database and close cursor & connection
        self.conn.commit()
        self.conn.close()