import csv
import datetime
import random
import string

from random import randint


PRODUCER_CNT = 30
SEIYUU_CNT = 65
rand_names = []
anime_std = []
anime = []
ep = []
tags = []
characters = []
anm_char = []
prs = []
def file_to_list(filename, listname):
    with open(filename, 'r') as f:
         for line in f:
            line = line.strip('\n')
            if not line:
                continue
            listname.append(line)

file_to_list('random_names.txt', rand_names)
file_to_list('anime_std.txt', anime_std)
file_to_list('anime.txt', anime)
file_to_list('episodes.txt', ep)
file_to_list('tags.txt', tags)
file_to_list('characters.txt', characters)
file_to_list('anime_character.txt', anm_char)
file_to_list('personalities.txt', prs)
def generate_producers():
    with open('producers.csv', 'w') as pcsv:
        fwriter = csv.writer(pcsv, delimiter=',', 
            quotechar='"', 
            quoting=csv.QUOTE_MINIMAL)
        fwriter.writerow(['name', 'birth_date', 'info'])
        for n in range(PRODUCER_CNT):
            name = rand_names[n]
            birth_date = datetime.date(1950 + randint(0, 45), randint(1, 12), randint(1, 28))
            info = "likes memes" if randint(1, 10**9) % 2 else "likes specific memes"
            fwriter.writerow([name, birth_date, info])

def generate_seiyuu():
     with open('seiyuu.csv', 'w') as pcsv:
        fwriter = csv.writer(pcsv, delimiter=',', 
            quotechar='"', 
            quoting=csv.QUOTE_MINIMAL)
        fwriter.writerow(['name', 'birth_date', 'gender', 'works_at'])
        for n in range(SEIYUU_CNT):
            name = rand_names[n]
            birth_date = datetime.date(1970 + randint(0, 30), randint(1, 12), randint(1, 28))
            gender = "M" if randint(1, 10**9) % 2 else "F"
            works_at = random.choice(anime_std)
            fwriter.writerow([name, birth_date, gender, works_at])

def generate_anime():
     with open('anime.csv', 'w') as acsv:
        fwriter = csv.writer(acsv, delimiter=',', 
            quotechar='"', 
            quoting=csv.QUOTE_MINIMAL)
        fwriter.writerow(['title', 'episodes', 'released_date',
            'end_date', 'producer_id', 'rating', 'studio'])
        with open('anime_tag.csv', 'w') as atcsv:
            awriter = csv.writer(atcsv, delimiter=',', 
            quotechar='"', 
            quoting=csv.QUOTE_MINIMAL)
            awriter.writerow(['anime_id', 'name', 'description'])
            n = 0
            for anm in anime:
                n += 1
                title = anm
                if randint(1, 10**9) % 2 :
                    episodes = randint(1, 10**9) % 48
                else:
                    episodes = random.choice(ep)
                released_date = datetime.date(2016 - randint(0, 20), randint(1, 12), randint(1, 28))
                end_date = datetime.date(max(int(released_date.year) + randint(0, 5), 2016),
                        randint(1, 12), randint(1, 28))
                producer_id = randint(1, PRODUCER_CNT)
                
                rating = round(random.uniform(0, 10.0), 2)
                studio = random.choice(anime_std)
                fwriter.writerow([title, episodes, released_date,
                end_date, producer_id, rating, studio])
                tag_number = randint(2, 7)
                for i in range(tag_number):
                    anime_id = n
                    name = random.choice(tags)
                    description = ""
                    awriter.writerow([anime_id, name, description])
   
def generate_characters():
     with open('character.csv', 'w') as acsv:
        fwriter = csv.writer(acsv, delimiter=',', 
            quotechar='"', 
            quoting=csv.QUOTE_MINIMAL)
        fwriter.writerow(['name', 'seiyuu_id', 'gender',
            'age', 'rating', 'waifu', 'personality'])
        with open('anime_character.csv', 'w') as accsv:
            awriter = csv.writer(accsv, delimiter=',', 
            quotechar='"', 
            quoting=csv.QUOTE_MINIMAL)
            awriter.writerow(['anime_id', 'character_id', 'relation'])
            n = 0
            for char in characters:
                n += 1
                name = char
                seiyuu_id = randint(1, SEIYUU_CNT)
                gender = "M" if randint(1, 10**9) % 2 else "F"
                age = randint(1, 10**9) % 30
                rating = round(random.uniform(0, 10.0), 2)
                waifu = 0
                personality = random.choice(prs)
                fwriter.writerow([name, seiyuu_id, gender,
            age, rating, waifu, personality])
                anm_number = randint(1, 3)
                for i in range(anm_number):
                    anime_id = randint(1, len(anime))
                    character_id = n
                    relation = random.choice(anm_char)
                    awriter.writerow([anime_id, character_id, relation])
   

if __name__ == '__main__':
    generate_producers()
    generate_seiyuu()
    generate_anime()
    generate_characters()
