#!/usr/bin/env python3

import patelin
from flask import Flask, jsonify, abort, request, make_response

server = Flask(__name__)

@server.route("/", methods=["GET", "OPTIONS"])
def main():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    else:
        data = {}
        data["name"] = patelin.generate_name()
        return _corsify_response(jsonify(data))

@server.route("/", methods=["POST", "PUT", "DELETE", "PATCH"])
def not_allowed():
    abort(405, description="Method is not allowed")

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

def _corsify_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    server.run(host='0.0.0.0')
