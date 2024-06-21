#!/usr/bin/env python

import sqlite3
import random

DB_FILE = 'tfidf.db'

CONNECTION = sqlite3.connect(DB_FILE)

def generate_name(source, n=2, max_token=3):
    res = '^'
    i = 0
    while res[-1] != '$':

        # Prends la fin
        key = res[-n:]
        # Filtre les fragments pour ne garder que ceux qui commencent par cette lettre
        candidates = dict((fragment, source[fragment]) for fragment in source if fragment.startswith(key))
        # Si l'on a atteint la limite, ne garde que les fragments terminaux
        if i >= max_token:
            candidates = dict((fragment, candidates[fragment]) for fragment in candidates if fragment.endswith('$'))

        # Calcule la probabilité associée à chaque fragment
        total = sum(candidates.values())

        # S'il n'existe aucun fragment valable, revient en arrière
        if total == 0:
            print("aaa")
            res = res[:-1]
            i -= 1
            continue

        # Choisis un fragment en respectant la distribution calculée auparavant
        res += random.choices(list(candidates.keys()), candidates.values())[0][len(key):]
        
        i += 1

    return res[1:-1]

def generate_source(coeffs):
    print("Generating source")
    source = {}
    cursor = CONNECTION.cursor()
    for region in coeffs:
        if coeffs[region] > 0:
            cursor.execute('SELECT frag_str, tfidf_val FROM tfidf JOIN regions ON tfidf.reg_id=regions.reg_id JOIN fragments ON fragments.frag_id = tfidf.frag_id WHERE reg_name = ?;', (region,))
            tfidf_values = cursor.fetchall()
            for frag_str, value in tfidf_values:
                if value > 0:
                    if frag_str not in source:
                        source[frag_str] = 0
                    source[frag_str] += coeffs[region] * value
    return source
