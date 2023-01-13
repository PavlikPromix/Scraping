import psycopg2
from dbconfig import *

db = psycopg2.connect(
    host="localhost",
    database=database,
    user=username,
    password=password
)

cur = db.cursor()
print("Search system (type !number to choose from results or !exit to exit)")

while True:
    srch = input("Search => ")
    choice = 0
    if srch[0] == '!':
        if srch[1:] == "exit":
            print("Exitting...")
            break
        if choice - 1 < len(data):
            choice = int(srch[1:])
            print(
                f"Price for the {data[choice-1][0]} is \xa3{data[choice-1][1]}")
            continue
        else:
            print("There is no such element in the database")

    cur.execute(
        f"SELECT * FROM data WHERE name LIKE '{srch.capitalize()}%' ORDER BY name")
    data = cur.fetchall()

    if len(data) == 0:
        print("There is no such element in the database")
        continue

    print(f"\nTotal occurrences: {len(data)}")

    for i in range(len(data)):
        row = data[i]
        print(f"{i+1}. {row[0]}")

cur.close()
db.close()
