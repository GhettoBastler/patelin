#!/usr/bin/env python3

import patelin
from flask import Flask, render_template

COEFFS = {
    'Auvergne-Rhône-Alpes': 0,
    'Hauts-de-France': 0,
    'Provence-Alpes-Côte d\'Azur': 0,
    'Grand Est': 1,
    'Occitanie': 0,
    'Normandie': 0,
    'Nouvelle-Aquitaine': 0,
    'Centre-Val de Loire': 0,
    'Bourgogne-Franche-Comté': 0,
    'Bretagne': 0,
    'Corse': 0,
    'Pays de la Loire': 0,
    'Île-de-France': 0,
    'Guadeloupe': 0,
    'Martinique': 0,
    'Guyane': 0,
    'La Réunion': 0,
    'Mayotte': 0,
}

SOURCE = patelin.generate_source(COEFFS)

server = Flask(__name__)

@server.route("/")
def main():
    # source = patelin.generate_source(COEFFS)
    # name = patelin.generate_name(source)
    name = patelin.generate_name(SOURCE)
    return render_template('base.html', name=name)

if __name__ == '__main__':
    server.run(host='0.0.0.0')
