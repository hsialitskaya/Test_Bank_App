from behave import *
import requests
from unittest_assertions import AssertEqual

assert_equal = AssertEqual()
URL = "http://127.0.0.1:5000"


@when('I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"')
def create_account(context, name, last_name, pesel):
    json_body = {
        "imie": f"{name}",
        "nazwisko": f"{last_name}",
        "pesel": pesel
    }
    create_resp = requests.post(URL + "/api/accounts", json=json_body)
    assert_equal(create_resp.status_code, 201)


@step('Number of accounts in registry equals: "{count}"')
def is_account_count_equal_to(context, count):
    response = requests.get(URL + "/api/accounts/count")
    assert_equal(response.status_code, 200)
    accounts = response.json()
    assert_equal(accounts["count"], int(count))


@step('Account with pesel "{pesel}" exists in registry')
def check_account_with_pesel_exists(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert_equal(response.status_code, 200)
    account = response.json()
    assert_equal(account["pesel"], pesel)

@step('Account with pesel "{pesel}" does not exist in registry')
def check_account_with_pesel_does_not_exist(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert_equal(response.status_code, 404)

@when('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    response = requests.delete(URL + f"/api/accounts/{pesel}")
    assert_equal(response.status_code, 200)


@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_field(context, field, pesel, value):
    if field not in ["name", "surname"]:
        raise ValueError(f"Invalid field: {field}. Must be 'name' or 'surname'.")
    json_body = { f"{field}": f"{value}" }
    response = requests.patch(URL + f"/api/accounts/{pesel}", json = json_body)
    assert_equal(response.status_code, 200)

@then('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def field_equals_to(context, pesel, field, value):
    field_mapping = {
        "name": "imie",
        "surname": "nazwisko"
    }
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert_equal(response.status_code, 200)
    account = response.json()
    assert_equal(account[field_mapping[field]], value)


