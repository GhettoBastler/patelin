#!/usr/bin/env python3

import patelin
from flask import Flask, render_template

server = Flask(__name__)

@server.route("/")
def main():
    name = patelin.generate_name()
    return render_template('base.html', name=name)

if __name__ == '__main__':
    server.run(host='0.0.0.0')
