import time

import psycopg2
from dbconfig import *
from selenium import webdriver
from selenium.webdriver.common.by import By

start = time.perf_counter()
driver = webdriver.Chrome()

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

page_number = 1
while page_number < 49:
    driver.get(f"https://scrapeme.live/shop/page/{page_number}")

    products = driver.find_elements(
        By.XPATH, '//a[@class="woocommerce-LoopProduct-link woocommerce-loop-product__link"]')

    for product in products:
        name, price = product.text.split()
        print(f"{name} => {price}")
        cursor.execute(f"INSERT INTO data (name, price) VALUES ('{name}', {price[1:]})")

    page_number += 1

db.commit()
cursor.close()
db.close()

end = time.perf_counter()
print(f"Elapsed time: {end-start}")
