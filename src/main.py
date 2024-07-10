#!/usr/bin/env python3

import patelin
from flask import Flask, jsonify, abort, request, make_response

server = Flask(__name__)


@server.route("/", methods=["GET", "OPTIONS"])
def main():
    data = {}
    data["name"] = patelin.generate_name()
    return jsonify(data)


@server.route("/", methods=["POST", "PUT", "DELETE", "PATCH"])
def not_allowed():
    abort(405, description="Method is not allowed")


if __name__ == '__main__':
    server.run()
