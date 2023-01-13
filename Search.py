import psycopg2
from dbconfig import *
from colorama import Fore

White = Fore.WHITE
Yellow = Fore.YELLOW
Green = Fore.GREEN
Red = Fore.RED

db = psycopg2.connect(
    host="localhost",
    database=database,
    user=username,
    password=password
)

cur = db.cursor()
print(f"{Green}Search {White}system (type !number to choose from results or !exit to exit)\n")

while True:
    srch = input(f"{Green}Search {White}=> ")
    choice = 0
    if srch[0] == '!':
        if srch[1:] == "exit":
            print(Yellow + "Exitting...")
            break
        if choice - 1 < len(data):
            choice = int(srch[1:])
            print(
                f"{White}Price for the {Green}{data[choice-1][0]} {White}is {Green}\xa3{data[choice-1][1]}")
            continue
        else:
            print(Red + "There is no such element in the database")

    cur.execute(
        f"SELECT * FROM data WHERE name LIKE '{srch.capitalize()}%' ORDER BY name")
    data = cur.fetchall()

    if len(data) == 0:
        print(Red + "There is no such element in the database")
        continue

    print(f"\n{White}Total occurrences: {Green}{len(data)}{White}")

    for i in range(len(data)):
        row = data[i]
        print(f"{i+1}. {row[0]}")

cur.close()
db.close()
