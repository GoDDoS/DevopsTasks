import psycopg2
import datetime
import csv



def add_seiyuu(name, birth_date, gender, rating, works_at):
    cur.execute("""
        INSERT INTO seiyuu (name, birth_date, gender, rating, works_at)
        VALUES (%s, %s, %c, %f, %s)
    """, (name, birth_date, gender, rating, works_at)
    )
    conn.commit()


def add_characters(name, seiyuu_name, birth_date, gender, age, rating, waifu, personality, info):
    cur.execute(
        "SELECT seiyuu_id IN seiyuu WHERE seiyuu.name = %s" % seiyuu_name
    )
    id = cur.fetchall()
    cur.execute("""
        INSERT INTO producers (name, seiyuu_id, gender, age, birth_date, rating, waifu, personality, info)
        VALUES (%s, %i, %c, %i, %s, %f, %i, %s, %s)
    """, (name, id[0], gender, age, birth_date, rating, waifu, personality, info)
    )
    conn.commit()


def add_producers(name, birth_date, info):
    cur.execute("""
        INSERT INTO producers (name, birth_date, info)
        VALUES (%s, %s, %s)
    """, (name, birth_date, info)
    )
    conn.commit()


def add_anime(title, type, re_date, end_date, producer_name, rating, std):
    cur.execute(
        "SELECT producer_id FROM producers WHERE producers.name = %s" % producer_name
    )
    id = cur.fetchall()
    cur.execute("""
        INSERT INTO anime (title, type, released_date, end_date, producer_id, rating, studio)
        VALUES (%s, %s, %s, %s, %i, %f, %s)
    """, (title, type, re_date, end_date, id[0], rating, std)
    )
    conn.commit()

'''
anime_file = open('anime.csv', "rb")
rdr = csv.reader(anime_file)
for line in rdr:
    title = line[0]
    type = line[1]
    re_date = datetime.date(line[2])
    end_date = datetime.date(line[3])
    rating = float(line[4])
    std = line[5]
    add_anime(title, type, re_date, end_date, rating, std)
'''


def add_anime(string):
    title = string
    str = ('type', 'released_date', 'end_date', 'producer_name', 'rating', 'studio')
    if string == '':
        print("Type title of the anime")
        title = input()
    array = {}
    for i, s in enumerate(str):
        print('Type ', s, " of the anime (type '-' if you don't know)")
        array[i] = input()
        if array[i] == '-':
            array[i] = 'DEFAULT'
    cur.execute("""
            INSERT INTO anime (title, type, released_date, end_date, producer_id, rating, studio)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (title, array[0], array[1], array[2], 1, array[4], array[5])
    )
    conn.commit()
    if string == '':
        print("Thank you for the information!\n")

def check_anime_in_DB(string):
    cur.execute(
        "SELECT COUNT(*) FROM anime WHERE anime.title = '%s' " % string
    )
    cnt = cur.fetchall()
    conn.commit()
    print(cnt[0][0])

def add_view():
    array = {}
    print("Type name of the anime")
    array[0] = input()
    cur.execute(
        "SELECT COUNT(*) FROM anime WHERE anime.title = '%s' " % (array[0])
    )

    cnt = cur.fetchall()
    conn.commit()
    if cnt[0][0] == 0:
        print("Sorry, we can't find the anime in the DB. Please, give us info about it")
        add_anime(array[0])

    print("Type date when you viewed the anime")
    array[1] = input()
    print("What is your rating for it?")
    array[2] = input()
    print("And who is your waifu?")

    array[3] = input()
    cur.execute(
        "UPDATE characters SET waifu = waifu + 1 WHERE name = '%s' " % (array[3])
    )
    conn.commit()
    cur.execute("""
        INSERT INTO personal_anime_list (title, view_date, personal_rating, waifu) VALUES (%s, %s, %s, %s)
    """, (array[0], array[1], array[2], array[3])
    )
    conn.commit()


def find_anime_tag(string):
    cur.execute("""
        SELECT anime.title FROM
        anime NATURAL JOIN tags
        WHERE description  = '%s'
    """, string
    )
    title_list = cur.fetchall()
    for line in title_list:
        print(line)


if __name__ == '__main__':
    conn = psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='postgres', port=5432)
    cur = conn.cursor()
    while 1:
        print("Type command ")
        command = input()
        if command == "add":
            add_view()
        elif command == "find":
            print("Type tag")
            string = input()
            find_anime_tag(string)
        elif command == "ch":
            print("Type anime title")
            string = input()
            check_anime_in_DB(string)
        elif command == "exit":
            break






