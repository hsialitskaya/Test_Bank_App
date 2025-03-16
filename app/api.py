from flask import Flask, request, jsonify
import os

from .AccountsRegistry import AccountsRegistry
from .PersonalAccount import PersonalAccount

app = Flask(__name__)

# stworzy konto osobiste i doda je do rejestru
@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Konto do stworzenia: {data}")

    if not all(el in data for el in ["imie", "nazwisko", "pesel"]):
        return jsonify({"Message": "Nie wszystkie dane sa wprowadzone"}), 400

    pesel=data["pesel"]
    account = AccountsRegistry.znajdz_account_po_peselu(pesel)
    if account is not None:
        return jsonify({"Message": "Pesel jest zajety"}), 409

    konto = PersonalAccount(data["imie"], data["nazwisko"], data["pesel"])
    AccountsRegistry.dodaj_account(konto)
    return jsonify({"Message": "Konto zostalo stworzone"}), 201



# zwróci dane konta (imię, nazwisko, pesel, saldo)
@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = AccountsRegistry.znajdz_account_po_peselu(pesel)
    if account is None:
        return jsonify({"Message": "Konto nie znalezione"}), 404

    return jsonify({
        "imie": account.imie,
        "nazwisko": account.nazwisko,
        "pesel": account.pesel,
        "saldo": account.saldo
    }), 200

# zaktualizowanie danych na koncie
@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    account = AccountsRegistry.znajdz_account_po_peselu(pesel)

    if account is None:
        return jsonify({"Message": "Konto nie znalezione"}), 404


    allowed_keys = {"name", "surname", "pesel", "saldo"}
    update_keys = set(data.keys()) & allowed_keys

    if not update_keys:
        return jsonify(
            {"Message": "Brak pól do aktualizacji. Podaj co najmniej jedno pole: imie, nazwisko, pesel, saldo"}), 400

    if "name" in data:
        account.imie = data["name"]
    if "surname" in data:
        account.nazwisko = data["surname"]
    if "pesel" in data:
        account.pesel = data["pesel"]
    if "saldo" in data:
        account.saldo = data["saldo"]

    return jsonify({
        "Message": "Konto zostalo zaktualizowane",
        "updated_account": {
            "name": account.imie,
            "surname": account.nazwisko,
            "pesel": account.pesel,
            "saldo": account.saldo
        }
    }), 200


@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account = AccountsRegistry.znajdz_account_po_peselu(pesel)

    if account is None:
        return jsonify({"Message": "Konto nie znalezione"}), 404

    AccountsRegistry.usun_account_po_peselu(pesel)
    return jsonify({"Message": "Konto zostalo usuniete"}), 200


def process_transfer(account, amount, transfer_type):
    if transfer_type == "incoming":
        account.przelew_wchodzacy(amount)
        return jsonify({"Message": "Zlecenie przyjeto do realizacji"}), 200

    elif transfer_type == "outgoing":
        if account.przelew_wychodzacy(amount):
            return jsonify({"Message": "Zlecenie przyjeto do realizacji"}), 200
        else:
            return jsonify({"Message": "Niewystarczające srodki na koncie"}), 422

    elif transfer_type == "express":
        if account.przelew_ekspresowy_wychodzacy(amount):
            return jsonify({"Message": "Zlecenie przyjeto do realizacji"}), 200
        else:
            return jsonify({"Message": "Niewystarczające srodki na koncie"}), 422


@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer(pesel):
    data = request.get_json()
    print(f"Zlecenie przelewu: {data}")

    if "amount" not in data or "type" not in data or data["amount"] < 0:
        return jsonify({"Message": "Brak wymaganych danych"}), 400

    account = AccountsRegistry.znajdz_account_po_peselu(pesel)
    if account is None:
        return jsonify({"Message": "Konto nie znalezione"}), 404

    amount = data["amount"]
    transfer_type = data["type"]

    if transfer_type not in ["incoming", "outgoing", "express"]:
        return jsonify({"Message": f"Nieznany typ transferu: {transfer_type}"}), 400

    return process_transfer(account, amount, transfer_type)

@app.route("/api/accounts/count", methods=['GET'])
def count_accounts():
    count = AccountsRegistry.policz_accounts()
    return jsonify({"count": count}), 200

@app.route("/api/accounts/clear", methods=['POST'])
def clear_accounts():
    AccountsRegistry.wyczysc_rejestr()
    return jsonify({"Message": "Rejestr został wyczyszcony"}), 200

@app.route("/api/accounts/backup", methods=['POST'])
def backup_accounts():
    filepath = request.json.get('filepath', '../test_backup.json')
    AccountsRegistry.zrzuc_dane_do_pliku(filepath)
    return jsonify({"Message": "Dane zostały zapisane", "filepath": filepath}), 200



@app.route("/api/accounts/restore", methods=['POST'])
def restore_accounts():
    filepath = request.json.get('filepath', '../test_backup.json')
    AccountsRegistry.zaladuj_dane_z_pliku(filepath)
    return jsonify({"Message": "Dane zostały załadowane", "filepath": filepath}), 200
