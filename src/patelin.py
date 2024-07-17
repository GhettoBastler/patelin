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


def check_first_part(name):
    """
    Checks that the first part of name isn't the begining of an actual
    town name"""
    first = name.replace('$', '-').replace('-', ' ').split()[0]
    return first not in FIRSTS


def do_markov(bodies, tails, n=2, min_token=3, max_token=4):
    print("Generating name")
    res = '^'
    checked = False
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

        if any(symbol in res for symbol in '-$ ') and not checked:
            # We have a hyphen. Check if the first word exists
            print("Checking that this doesn\'t look to much like a real name")
            if not check_first_part(res[1:]):
                print("Already exists. Retrying")
                # Restart
                i = 0
                res = '^'
                continue
            else:
                print("All good. Continuing")
                # We can continue
                checked = True

    return res[1:-1]


def generate_name(n=3, min_token=3, max_token=4):
    bodies, tails = BASE_SOURCE
    name = do_markov(bodies, tails, n, min_token, max_token)
    return name
