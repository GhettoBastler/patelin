#!/usr/bin/env python

import sqlite3
import pytest
from main import server


@pytest.fixture()
def communes():
    # connection = sqlite3.connect('tfidf.db')
    # cursor = connection.cursor()
    # cursor.execute('SELECT com_nom FROM communes;')
    # result = cursor.fetchall()
    # yield [row[0] for row in result]
    # connection.close()
    with open('communes.txt') as f:
        communes = [name.strip() for name in f.readlines()]
    return communes


@pytest.fixture()
def client():
    return server.test_client()


def test_get(client):
    response = client.get("/")
    assert response.status_code == 200


def test_json_response(client):
    response = client.get("/")
    assert response.json


def test_contains_name(client):
    response = client.get("/")
    assert response.json["name"]


def test_name_does_not_exist(client, communes):
    response = client.get("/")
    name = response.json["name"]
    assert name not in communes


def test_unknown_url(client):
    response = client.get("/unknown")
    assert response.status_code == 404


def test_post(client):
    response = client.post("/")
    assert response.status_code == 405


def test_put(client):
    response = client.put("/")
    assert response.status_code == 405


def test_delete(client):
    response = client.delete("/")
    assert response.status_code == 405


def test_patch(client):
    response = client.patch("/")
    assert response.status_code == 405
