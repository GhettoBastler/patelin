#!/usr/bin/env python

import pickle
import random
import sqlite3


SOURCE_FILE = 'base_source.pickle'
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


def do_markov(source, n=2, max_token=3):
    print("Generating name")
    res = '^'
    i = 0
    while res[-1] != '$':

        # Prends la fin
        key = res[-n:]
        # Filtre les fragments pour ne garder que ceux qui commencent par
        # cette lettre
        candidates = dict(
            (fragment, source[fragment]) for fragment in source
            if fragment.startswith(key)
        )
        # Si l'on a atteint la limite, ne garde que les fragments terminaux
        if i >= max_token:
            candidates = dict(
                (fragment, candidates[fragment]) for fragment in candidates
                if fragment.endswith('$')
            )

        # Calcule la probabilité associée à chaque fragment
        total = sum(candidates.values())

        # S'il n'existe aucun fragment valable, revient en arrière
        if total == 0:
            res = res[:-1]
            i -= 1
            continue

        # Choisis un fragment en respectant la distribution calculée auparavant
        res += random.choices(
            list(candidates.keys()), candidates.values()
        )[0][len(key):]
        i += 1

    return res[1:-1]


def generate_source(connection, coeffs):
    print("Generating source")
    source = {}
    cursor = connection.cursor()
    for region in coeffs:
        if coeffs[region] > 0:
            cursor.execute(
                'SELECT frag_str, tfidf_val'
                'FROM tfidf JOIN regions ON tfidf.reg_id=regions.reg_id'
                'JOIN fragments ON fragments.frag_id = tfidf.frag_id'
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


def generate_name(coeffs=COEFFS, n=3, max_token=3):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    if coeffs == COEFFS:
        source = BASE_SOURCE
    else:
        source = generate_source(connection, coeffs)
    while True:
        name = do_markov(source, n, max_token)
        cursor.execute(
            'SELECT * FROM communes'
            'WHERE com_nom LIKE ?;',
            (name+'%',)
        )
        if not cursor.fetchone():
            return name
        else:
            print('Name already exists, retrying')
