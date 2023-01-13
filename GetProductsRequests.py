import time

import psycopg2
import requests
from bs4 import BeautifulSoup
from dbconfig import *

start = time.perf_counter()

db = psycopg2.connect(
    host="localhost",
    user=username,
    password=password
)

db.autocommit = True

cursor = db.cursor()

# creating a new database if it doesn't exist yet
cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{database}'") # cursor.fetchone() returns true or false
if not cursor.fetchone():
    cursor.execute(f"CREATE DATABASE {database}")

# connecting to the database
db = psycopg2.connect(
    host="localhost",
    user=username,
    password=password,
    database=database
)

cursor = db.cursor()

# creating a new table if it doesn't exist yet
cursor.execute(
    "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'data')")
if not cursor.fetchone()[0]:
    cursor.execute("CREATE TABLE data (name VARCHAR(255), price INTEGER)")


page = 1
while page <= 48:
    response = requests.get(f'https://scrapeme.live/shop/page/{page}')
    soup = BeautifulSoup(response.text, 'html.parser')

    results = soup.select(
        'a.woocommerce-LoopProduct-link.woocommerce-loop-product__link')
    for result in results:
        name, price = result.text.split()
        print(f"{name} => {price}")
        cursor.execute(f"INSERT INTO data (name, price) VALUES ('{name}', {price[1:]});")

    page += 1

db.commit()
cursor.close()
db.close()

end = time.perf_counter()
print(f"Elapsed time: {end-start}")