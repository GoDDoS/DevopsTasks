#from graphic import *
import psycopg2
import datetime
import csv

conn = psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='postgres', port=5432)
cur = conn.cursor()


def add_seiyuu(name, birth_date, gender, works_at):
    cur.execute("""
        INSERT INTO seiyuu (name, birth_date, gender, works_at)
        VALUES ('%s', '%s', '%s', '%s')
    """ % (name, birth_date, gender, works_at)
    )
    conn.commit()


def add_characters(name, seiyuu_id, gender, age, rating, waifu, personality):
    cur.execute("""
        INSERT INTO characters(name, seiyuu_id, gender, age, rating, waifu, personality)
        VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')
    """ % (name, seiyuu_id, gender, age, rating, waifu, personality)
    )
    conn.commit()


def add_producers(name, birth_date, info):
    cur.execute("""
        INSERT INTO producers (name, birth_date, info)
        VALUES ('%s', '%s', '%s')
    """ % (name, birth_date, info)
    )
    conn.commit()


def add_anime(title, episodes, re_date, end_date, producer_id, rating, std):
    cur.execute("""
        INSERT INTO anime (title, episodes, released_date, end_date, producer_id, rating, studio)
        VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')
    """ % (title, episodes, re_date, end_date, producer_id, rating, std)
    )
    conn.commit()


def add_anime_char(anime_id, char_id, relation):
    cur.execute("""
        INSERT INTO anime_character (anime_id, character_id, relation)
        VALUES ('%s', '%s', '%s')
    """ % (anime_id, char_id, relation)
    )
    conn.commit()


def add_anime_tag(anime_id, name, description):
    cur.execute("""
        INSERT INTO tags (anime_id, name, description)
        VALUES ('%s', '%s', '%s')
    """ % (anime_id, name, description)
    )
    conn.commit()


def check_anime_in_DB(string):
    cur.execute(
        "SELECT COUNT(*) FROM anime WHERE anime.title = %s ", [string[:-1]]
    )
    cnt = cur.fetchall()
    conn.commit()
    return cnt[0][0]


def add_view(title):
    array = {}
    array[0] = title
    cur.execute(
        "SELECT COUNT(*) FROM anime WHERE anime.title = '%s' " % (array[0])
    )

    cnt = cur.fetchall()
    conn.commit()
    if cnt[0][0] == 0:
        print("Sorry, we can't find the anime in the DB. Please, give us info about it")
        add_user_anime(array[0])

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
    """ % (array[0], array[1], array[2], array[3])
    )
    conn.commit()


def add_personal_list(title, personal_rating, view_date, waifu):
    cur.execute("""
        INSERT INTO personal_anime_list (title, personal_rating, view_date, waifu)
        VALUES ('%s', '%s', '%s', '%s')
    """ % (title[:-1], personal_rating[:-1], view_date[:-1], waifu[:-1])
    )
    conn.commit()


def find_anime_tag(string):
    cur.execute("""
        SELECT anime.title FROM
        anime NATURAL JOIN tags
        WHERE description  = %s
        LIMIT 10
    """ % [string[:-1]]
    )
    title_list = cur.fetchall()
    for line in title_list:
        print(line)


def find_anime_by_tag(tag_name):
    cur.execute("""
        SELECT *
        FROM anime NATURAL JOIN tags
        WHERE tags.name = %s
        LIMIT 10
    """, [tag_name[:-1]]
    )
    anm = cur.fetchall()
    return anm


def find_anime_by_title(anime_title):
    cur.execute(
        "SELECT COUNT(*) FROM anime WHERE anime.title=%s", [anime_title[:-1]]
    )
    cnt = cur.fetchall()
    if cnt[0][0] == 0:
        string = "Don't have the anime in the database"
        anm = [[] * 0]
        anm[0] = string
        return anm
    else:
        cur.execute("SELECT * FROM anime WHERE title = %s", [anime_title[:-1]]
        )
    anm = cur.fetchall()
    return anm


def find_ch_by_name(ch_name):
    cur.execute("""
        SELECT * FROM characters WHERE characters.name = %s
    """, [ch_name[:-1]]
    )
    anm = cur.fetchall()
    return anm


def top_anime():
    cur.execute("""
		SELECT * FROM anime ORDER BY rating DESC LIMIT 10
    """
    )
    anm = cur.fetchall()
    return anm


def my_list():
    cur.execute("""
        SELECT * FROM personal_anime_list
        ORDER BY view_date
    """
    )
    anm = cur.fetchall()
    return anm


def inf_by_seiyuu(seiyuu_name):
    cur.execute("""
		WITH char AS (
			SELECT character_id, character_name
			FROM characters JOIN seiyuu
		        ON seiyuu.seiyuu_id = characters.seiyuu_id
		    WHERE seiyuu.name = %s
		), SELECT anime.name, character.name, anime_character.relation
		FROM (char NATURAL JOIN anime_character) NATURAL JOIN anime
	""", [seiyuu_name[:-1]]
    )
    anm = cur.fetchall()
    return anm


def drop_it_all():
    cur.execute("""
        DROP TABLE IF EXISTS seiyuu CASCADE;
        DROP TABLE IF EXISTS characters CASCADE;
        DROP TABLE IF EXISTS producers CASCADE;
        DROP TABLE IF EXISTS anime CASCADE;
        DROP TABLE IF EXISTS personal_anime_list CASCADE;
        DROP TABLE IF EXISTS anime_character CASCADE;
        DROP TABLE IF EXISTS tags CASCADE;
    """
    )
    conn.commit()


def clear_list():
    cur.execute("""
        DROP TABLE IF EXISTS personal_anime_list CASCADE;
        CREATE TABLE personal_anime_list (
        title TEXT REFERENCES anime(title),
        personal_rating INTEGER DEFAULT(0),
        view_date DATE DEFAULT NULL,
        waifu TEXT REFERENCES characters(name)
        );
    """
    )
    conn.commit()

if __name__ == '__main__':
    seiyuu_file = open('seiyuu.csv')
    rdr = csv.DictReader(seiyuu_file)
    for i, line in enumerate(rdr):
        name = line['name']
        date = line['birth_date']
        gender = line['gender']
        std = line['works_at']
        add_seiyuu(name, date, gender, std)

    character_file = open('character.csv')
    rdr = csv.DictReader(character_file)
    for i, line in enumerate(rdr):
        name = line['name']
        seiyuu_id = line['seiyuu_id']
        gender = line['gender']
        age = line['age']
        rating = float(line['rating'])
        waifu = int(line['waifu'])
        personality = line['personality']
        add_characters(name, seiyuu_id, gender, age, rating, waifu, personality)

    producer_file = open('producers.csv')
    rdr = csv.DictReader(producer_file)
    for i, line in enumerate(rdr):
        name = line['name']
        date = line['birth_date']
        info = line['info']
        add_producers(name, date, info)

    anime_file = open('anime.csv')
    rdr = csv.DictReader(anime_file)
    for i, line in enumerate(rdr):
        title = line['title']
        episodes = line['episodes']
        re_date = line['released_date']
        end_date = line['end_date']
        prod_id = line['producer_id']
        rating = float(line['rating'])
        std = line['studio']
        add_anime(title, episodes, re_date, end_date, prod_id, rating, std)

    an_ch_file = open('anime_character.csv')
    rdr = csv.DictReader(an_ch_file)
    for i, line in enumerate(rdr):
        an_id = line['anime_id']
        ch_id = line['character_id']
        relation = line['relation']
        add_anime_char(an_id, ch_id, relation)

    an_tag_file = open('anime_tag.csv')
    rdr = csv.DictReader(an_tag_file)
    for i, line in enumerate(rdr):
        an_id = line['anime_id']
        name = line['name']
        description = line['description']
        add_anime_tag(an_id, name, description)

    # root = Tk()
    # root.mainloop()
    ''' while 1:
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
            break '''






