from behave import *
import requests
from unittest_assertions import AssertEqual

assert_equal = AssertEqual()
URL = "http://127.0.0.1:5000"

@given('Użytkownik posiada konto bankowe o numerze PESEL {pesel}')
def find_account(context, pesel):
    create_resp = requests.get(URL + f"/api/accounts/{pesel}")
    assert_equal(create_resp.status_code, 200)
    context.pesel = pesel


@step('Saldo użytkownika na koncie wynosi {balance} zł')
def update_balance(context, balance):
    json_body = {
        "saldo": int(balance)
    }
    response = requests.patch(URL + f"/api/accounts/{context.pesel}", json=json_body)
    assert_equal(response.status_code, 200)
    context.saldo = int(balance)


@when('Użytkownik otrzymuje przelew przychodzący w wysokości {amount} zł')
def incoming_transfer(context, amount):
    json_body = {
        "amount": int(amount),
        "type": "incoming"
    }
    transfer_resp = requests.post(URL + f"/api/accounts/{context.pesel}/transfer", json=json_body)
    assert_equal(transfer_resp.status_code, 200)


@when('Użytkownik zleca przelew {typ_przeliewu} w wysokości {amount} zł')
def outgoing_transfer(context, amount, typ_przeliewu):
    if typ_przeliewu == "wychodzący":
        json_body = {
            "amount": int(amount),
            "type": "outgoing"
        }
        transfer_resp = requests.post(URL + f"/api/accounts/{context.pesel}/transfer", json=json_body)
        context.transfer_resp = transfer_resp
        if int(amount) > context.saldo:
            assert_equal(transfer_resp.status_code, 422)
        else:
            assert_equal(transfer_resp.status_code, 200)

    elif typ_przeliewu == "ekspresowy":
        json_body = {
            "amount": int(amount),
            "type": "express"
        }
        transfer_resp = requests.post(URL + f"/api/accounts/{context.pesel}/transfer", json=json_body)
        context.transfer_resp = transfer_resp
        if int(amount) > context.saldo + 1:
            assert_equal(transfer_resp.status_code, 422)
        else:
            assert_equal(transfer_resp.status_code, 200)


@when('Użytkownik zleca przelew o niepoprawnym typie {type}')
def incorrect_transfer_type(context, type):
    json_body = {
        "amount": 100,
        "type": type
    }
    transfer_resp = requests.post(URL + f"/api/accounts/{context.pesel}/transfer", json=json_body)
    context.transfer_resp = transfer_resp


@step('Saldo użytkownika na koncie powinno wynosić {balance} zł')
def check_balance(context, balance):
    response = requests.get(URL + f"/api/accounts/{context.pesel}")
    assert_equal(response.status_code, 200)
    account = response.json()
    assert_equal(account["saldo"], int(balance))


@then('System powinien zwrócić komunikat: {message}')
def check_transfer_message(context, message):
    assert_equal(context.transfer_resp.json().get("Message"), message)




