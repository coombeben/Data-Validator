from os.path import join as pjoin, dirname
import sqlite3
import csv

from consts import INSTANCE_PATH


def populate_database(db_uri):
    """Initialises the database and populates with the initial dogs"""
    db_fldr = pjoin(INSTANCE_PATH, 'db')

    con = sqlite3.connect(db_uri)
    cur = con.cursor()
    with open(pjoin(db_fldr, 'schema.sql'), 'r') as sql_file:
        init_sql = sql_file.read()

    cur.execute(init_sql)

    with open(pjoin(db_fldr, 'breeds.csv'), 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        skip_header = True
        for row in reader:
            if skip_header:
                skip_header = False
            else:
                to_db = [row[0], row[1], 0]
                cur.execute('INSERT INTO breeds (breed, query, search_count) VALUES (?, ?, ?);', to_db)

    con.commit()
    con.close()
