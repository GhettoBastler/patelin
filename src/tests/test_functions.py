import pytest
import pickle
from patelin import check_first_part


@pytest.fixture()
def firsts():
    with open('firsts.pickle', 'rb') as f:
        firsts = pickle.load(f)
    return firsts


def test_invalidates_existing_names(firsts):
    assert check_first_part('SAUVIAT-EN-LAYE') is False
    assert check_first_part('VILLERUPT$') is False
    assert check_first_part('NANCY SUR SEINE') is False
