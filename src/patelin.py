#!/usr/bin/env python

import pickle
import random
import sqlite3


# SOURCE_FILE = 'base_source.pickle'
SOURCE_FILE = 'splited_source.pickle'
DB_FILE = 'tfidf.db'
COEFFS = {
    'Auvergne-Rhône-Alpes': 1,
    'Hauts-de-France': 1,
    'Provence-Alpes-Côte d\'Azur': 1,
    'Grand Est': 1,
    'Occitanie': 1,
    'Normandie': 1,
    'Nouvelle-Aquitaine': 1,
    'Centre-Val de Loire': 1,
    'Bourgogne-Franche-Comté': 1,
    'Bretagne': 1,
    'Corse': 1,
    'Pays de la Loire': 1,
    'Île-de-France': 1,
    'Guadeloupe': 1,
    'Martinique': 1,
    'Guyane': 1,
    'La Réunion': 1,
    'Mayotte': 1,
}


print("Importing base sources")
with open(SOURCE_FILE, 'rb') as file_object:
    BASE_SOURCE = pickle.load(file_object)


def do_markov(bodies, tails, n=2, min_token=3, max_token=4):
    print("Generating name")
    res = '^'
    print(res)
    i = 0
    while res[-1] != '$':
        # Use the tail of the current name as the key
        key = res[-n:]
        # If we reached the token limit, only use the final fragments
        if i >= max_token-1:
            fragment_pool = tails
        elif i <= min_token:
            # If the name is too short, don't use the final fragments
            fragment_pool = bodies

        # Keep only the fragments that starts with this key
        candidates = dict(
            (fragment, fragment_pool[fragment]) for fragment in fragment_pool
            if fragment.startswith(key)
        )

        # Check that there are still available fragments
        total = sum(candidates.values())
        if total == 0:
            # Else, remove one character and retry
            res = res[:-1]
            i -= 1
            continue

        # Pick a fragment
        res += random.choices(
            list(candidates.keys()), candidates.values()
        )[0][len(key):]
        i += 1
        print(res)

    return res[1:-1]


def generate_source(connection, coeffs):
    print("Generating source")
    source = {}
    cursor = connection.cursor()
    for region in coeffs:
        if coeffs[region] > 0:
            cursor.execute(
                'SELECT frag_str, tfidf_val '
                'FROM tfidf JOIN regions ON tfidf.reg_id=regions.reg_id '
                'JOIN fragments ON fragments.frag_id = tfidf.frag_id '
                'WHERE reg_name = ?;',
                (region,)
            )
            tfidf_values = cursor.fetchall()
            for frag_str, value in tfidf_values:
                if value > 0:
                    if frag_str not in source:
                        source[frag_str] = 0
                    source[frag_str] += coeffs[region] * value
    return source


def split_source(source):
    tails = dict(
        (fragment, source[fragment]) for fragment in source
        if fragment.endswith('$')
    )
    bodies = dict(
        (fragment, source[fragment]) for fragment in source
        if fragment not in tails
    )
    return tails, bodies


def generate_name(coeffs=COEFFS, n=3, min_token=3, max_token=4):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    if coeffs == COEFFS:
        bodies, tails = BASE_SOURCE
    else:
        source = generate_source(connection, coeffs)
        bodies, tails = split_source(source)
    while True:
        name = do_markov(bodies, tails, n, min_token, max_token)
        cursor.execute(
            'SELECT * FROM communes '
            'WHERE com_nom LIKE ?;',
            (name+'%',)
        )
        if not cursor.fetchone():
            return name
        else:
            print('Name already exists, retrying')
