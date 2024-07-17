#!/usr/bin/env python

import pytest
import pickle
from main import server


@pytest.fixture()
def firsts():
    with open('firsts.pickle', 'rb') as f:
        firsts = pickle.load(f)
    return firsts


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


def test_first_word_does_not_exist(client, firsts):
    response = client.get("/")
    name = response.json["name"]
    first_word = name.split('-')[0].split(' ')[0]
    assert first_word not in firsts


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
