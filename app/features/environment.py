import requests
from unittest_assertions import AssertEqual

assert_equal = AssertEqual()
URL = "http://127.0.0.1:5000"

def before_scenario(context, scenario):
    if 'transfer' in scenario.tags:
        account_data = {
            "imie": "Dariusz",
            "nazwisko": "Januszewski",
            "pesel": "98765432109"
        }
        create_resp = requests.post(URL + "/api/accounts", json=account_data)
        assert_equal(create_resp.status_code, 201)

def after_scenario(context, scenario):
    if 'transfer' in scenario.tags:
        pesel = "98765432109"
        delete_resp = requests.delete(URL + f"/api/accounts/{pesel}")
        assert_equal(delete_resp.status_code, 200)


def after_all(context):
    response = requests.post(URL + "/api/accounts/clear")
    assert_equal(response.status_code, 200)
    if response.status_code != 200:
        raise AssertionError("Nie udało się wyczyścić rejestru")
