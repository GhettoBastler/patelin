#!/usr/bin/env python

import pickle
import random


SOURCE_FILE = 'splited_source.pickle'
FIRSTS_FILE = 'firsts.pickle'


print("Importing base sources")
with open(SOURCE_FILE, 'rb') as file_object:
    BASE_SOURCE = pickle.load(file_object)

print("Importing first names")
with open(FIRSTS_FILE, 'rb') as file_object:
    FIRSTS = pickle.load(file_object)


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


def check_name(name):
    first_part = name.split('-')[0].split(' ')[0]
    return first_part not in FIRSTS


def generate_name(n=3, min_token=3, max_token=4):
    bodies, tails = BASE_SOURCE
    while True:
        name = do_markov(bodies, tails, n, min_token, max_token)
        if check_name(name):
            return name
        else:
            print('Name already exists, retrying')
