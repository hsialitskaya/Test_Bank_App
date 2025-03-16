import unittest
import requests
from parameterized import parameterized

class TestAPI_transfers(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000/api/accounts"
    account_data = {
        "imie": "Dariusz",
        "nazwisko": "Januszewski",
        "pesel": "98765432109"
    }

    def setUp(self):
        response = requests.post(self.BASE_URL, json=self.account_data)
        self.assertEqual(response.status_code, 201, "Niepoprawny kod błędu przy tworzeniu konta")

    def tearDown(self):
        response = requests.delete(f"{self.BASE_URL}/{self.account_data['pesel']}")
        self.assertEqual(response.status_code, 200, "Nie udało się usunąć konta z API")

    @parameterized.expand([
        ("test_konto_nie_istnieje", "00000000000", 500, "incoming", 404),
        ("test_poprawny_typ_przelewu_wchodzacy", account_data["pesel"], 500, "incoming", 200),
        ("test_poprawny_typ_przelewu_wychodzacy", account_data["pesel"], 500, "outgoing", 200),
        ("test_poprawny_typ_przelewu_ekspresowy", account_data["pesel"], 500, "express", 200),
        ("test_nie_poprawny_typ_przelewu", account_data["pesel"], 500, "aaaaaaa", 400),
        ("test_wychodzacy_niewystarcza_srodkow", account_data["pesel"], 50000, "outgoing", 422),
        ("test_ekspresowy_niewystarcza_srodkow", account_data["pesel"], 50000, "express", 422)
    ])

    def test_pzelew(self, name, pesel, amount, type, expected_kod):
        print(f"Test: {name}")
        data = {
            "amount": amount,
            "type": type
        }
        if type == "outgoing" or type == "express":
            nowe = {
                "saldo": 500
            }
            response = requests.patch(f"{self.BASE_URL}/{pesel}", json=nowe)
            self.assertEqual(response.status_code, 200, "Niepoprawny kod błędu")
        response = requests.post(f"{self.BASE_URL}/{pesel}/transfer", json=data)
        self.assertEqual(response.status_code, expected_kod, "Niepoprawny kod błędu")

    @parameterized.expand([
        ("test_poprawny_typ_przelewu_wchodzacy", account_data["pesel"], 500, "incoming", "Zlecenie przyjeto do realizacji"),
        ("test_poprawny_typ_przelewu_wychodzacy", account_data["pesel"], 500, "outgoing", "Zlecenie przyjeto do realizacji"),
        ("test_poprawny_typ_przelewu_ekspresowy", account_data["pesel"], 500, "express", "Zlecenie przyjeto do realizacji")
    ])
    def test_wiadomosc(self, name, pesel, amount, type, expected_message):
        print(f"Test: {name}")
        if type in ["outgoing", "express"]:
            account_data = {"saldo": amount + 1}
            response = requests.patch(f"{self.BASE_URL}/{pesel}", json=account_data)
            self.assertEqual(response.status_code, 200, "Niepoprawny kod odpowiedzi dla ustawienia salda")
        data = {
            "amount": amount,
            "type": type
        }
        response = requests.post(f"{self.BASE_URL}/{pesel}/transfer", json=data)
        self.assertEqual(response.json()["Message"], expected_message, "Niepoprawna wiadomość zwrócona przez API")
    @parameterized.expand([
        ("test_przelew_wchodzacy_kwota", account_data["pesel"], 500, "incoming",
         500),
        ("test_przelew_wychodzacy_kwota", account_data["pesel"], 100, "outgoing",
         400),
        ("test_przelew_wychodzacy_kwota", account_data["pesel"], 100, "express",
         399),
    ])
    def test_kwota(self, name, pesel, amount, type, expected_amount):
        print(f"Test: {name}")
        data = {
            "amount": amount,
            "type": type
        }
        if type == "outgoing" or type == "express":
            nowe = {
                "saldo": 500
            }
            response = requests.patch(f"{self.BASE_URL}/{pesel}", json=nowe)
            self.assertEqual(response.status_code, 200, "Niepoprawny kod błędu")

        response = requests.post(f"{self.BASE_URL}/{self.account_data['pesel']}/transfer", json=data)
        self.assertEqual(response.status_code, 200, "Niepoprawny kod błędu")
        response = requests.get(f"{self.BASE_URL}/{self.account_data['pesel']}")
        updated_balance = response.json().get("saldo")
        self.assertEqual(updated_balance, expected_amount, "Niepoprawne saldo")

    def test_seria_przelewow(self):
        data1 = {
            "amount": 500,
            "type": "incoming"
        }
        data2 = {
            "amount": 500,
            "type": "outgoing"
        }

        # Pierwszy przelew
        response1 = requests.post(f"{self.BASE_URL}/{self.account_data['pesel']}/transfer", json=data1)
        self.assertEqual(response1.status_code, 200, "Niepoprawny kod błędu")

        # Drugi przelew
        response2 = requests.post(f"{self.BASE_URL}/{self.account_data['pesel']}/transfer", json=data2)
        self.assertEqual(response2.status_code, 200, "Niepoprawny kod błędu")

        # Sprawdzanie salda po dwóch przelewach
        response = requests.get(f"{self.BASE_URL}/{self.account_data['pesel']}")
        self.assertEqual(response.json()["saldo"], 0, "Niepoprawne saldo")

