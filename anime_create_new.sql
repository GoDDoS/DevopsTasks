DROP TABLE IF EXISTS seiyuu CASCADE;
CREATE TABLE seiyuu (
    seiyuu_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    birth_date DATE DEFAULT NULL,
    gender CHAR(1) CHECK(gender = 'M' OR gender = 'F'),
    works_at TEXT DEFAULT NULL
);

DROP TABLE IF EXISTS characters CASCADE;
CREATE TABLE characters (
    character_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    seiyuu_id INTEGER REFERENCES seiyuu(seiyuu_id),
    gender TEXT DEFAULT NULL,
    age INTEGER DEFAULT NULL,
    rating FLOAT DEFAULT(0),
    waifu INTEGER DEFAULT(0),
    personality TEXT DEFAULT NULL,
    UNIQUE (name)
);

DROP TABLE IF EXISTS producers CASCADE;
CREATE TABLE producers (
    producer_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    birth_date DATE DEFAULT NULL,
    info TEXT DEFAULT NULL
);

DROP TABLE IF EXISTS anime CASCADE;
CREATE TABLE anime (
    anime_id SERIAL PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
    episodes TEXT DEFAULT NULL,
    released_date DATE DEFAULT NULL,
    end_date DATE DEFAULT NULL,
    producer_id INTEGER REFERENCES producers(producer_id),
    rating FLOAT DEFAULT(0),
    studio TEXT DEFAULT NULL,
    UNIQUE (title)
);

DROP TABLE IF EXISTS anime_character CASCADE;
CREATE TABLE anime_character (
    anime_id INTEGER NOT NULL REFERENCES anime(anime_id),
    character_id INTEGER NOT NULL REFERENCES characters(character_id),
    relation TEXT DEFAULT NULL
);

DROP TABLE IF EXISTS tags CASCADE;
CREATE TABLE tags (
    anime_id INTEGER REFERENCES anime(anime_id),
    name TEXT NOT NULL,
    description TEXT DEFAULT NULL
);

DROP TABLE IF EXISTS personal_anime_list CASCADE;
CREATE TABLE personal_anime_list (
    title TEXT REFERENCES anime(title),
    personal_rating INTEGER DEFAULT(0),
    view_date DATE DEFAULT NULL,
    waifu TEXT REFERENCES characters(name)
    -- link waifu with characters.name, then link character_id of this name with 
    -- anime_id through anime_character, 
    -- then select anime which title is the same as personal_anime_list.title
);
