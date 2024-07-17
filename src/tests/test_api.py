#!/usr/bin/env python

import pytest
from main import server


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
