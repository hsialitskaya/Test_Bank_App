import unittest
import requests
from parameterized import parameterized
import os
import json


class TestAPI(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000/api/accounts"
    account_data = {
        "imie": "Dariusz",
        "nazwisko": "Januszewski",
        "pesel": "12345678901"
    }
    backup_filepath = 'test_backup.json'

    def setUp(self):
        response = requests.post(self.BASE_URL, json=self.account_data)
        self.assertEqual(response.status_code, 201, "Niepoprawny kod błędu przy tworzeniu konta")

    def tearDown(self):
        pesel = self.account_data["pesel"]
        if requests.get(f"{self.BASE_URL}/{pesel}").status_code != 404:
            response = requests.delete(f"{self.BASE_URL}/{pesel}")
            self.assertEqual(response.status_code, 200, "Nie udało się usunąć konta z API")

    @parameterized.expand([
        ("test_tworzenie_konta_pesel_zajety", {
            "imie": "Jan",
            "nazwisko": "Kowalski",
            "pesel": "12345678901"
        }, 409),
        ("test_tworzenie_konta_zle_dane", {
            "imie": "Dariusz",
            "nazwisko": "Januszewski",
        }, 400),
    ])
    def test_tworzenie(self, name, data, expected_kod):
        print(f"Test: {name}")
        response = requests.post(self.BASE_URL, json=data)
        self.assertEqual(response.status_code, expected_kod, "Niepoprawny kod błędu")


    @parameterized.expand([
        ("test_znajdz_account_po_peselu_istnieje", "12345678901", 200),
        ("test_znajdz_account_po_peselu_nie_istnieje", "00000000000", 404)
    ])
    def test_znajdowanie(self, name, pesel, expected_kod):
        print(f"Test: {name}")
        response = requests.get(f"{self.BASE_URL}/{pesel}")
        self.assertEqual(response.status_code, expected_kod, "Niepoprawny kod błędu")

    def test_znajdz_account_po_peselu_sprawdzenie_danych(self):
        account = requests.get(f"{self.BASE_URL}/{self.account_data['pesel']}").json()
        self.assertEqual(account["imie"], "Dariusz", "Niepoprawne imie")
        self.assertEqual(account["nazwisko"], "Januszewski", "Niepoprawne nazwisko")
        self.assertEqual(account["pesel"], self.account_data["pesel"], "Niepoprawny pesel")
        self.assertEqual(account["saldo"], 0, "Niepoprawne saldo")

    @parameterized.expand([
        ("test_aktualizacja_account_dobrze", "12345678901", {"name": "Olaf", "saldo": 8000}, 200),
        ("test_aktualizacja_account_zle", "00000000000", {"name": "Olaf", "saldo": 8000}, 404),
    ])
    def test_aktualizacja(self, name, pesel, dane, expected_kod):
        print(f"Test: {name}")
        response = requests.patch(f"{self.BASE_URL}/{pesel}", json=dane)
        self.assertEqual(response.status_code, expected_kod, "Niepoprawny kod błędu")

    def test_aktualizacja_account_dobrze_sprawdzenie_danych(self):
        account = requests.get(f"{self.BASE_URL}/{self.account_data['pesel']}").json()
        nowe = {
            "name": "Olaf",
            "saldo": 8000
        }
        requests.patch(f"{self.BASE_URL}/{self.account_data['pesel']}", json=nowe)
        response_data = requests.get(f"{self.BASE_URL}/{self.account_data['pesel']}").json()
        self.assertEqual(response_data["imie"], "Olaf", "Niepoprawne imie")
        self.assertEqual(response_data["saldo"], 8000, "Niepoprawne saldo")
        self.assertEqual(response_data["pesel"], account["pesel"], "Niepoprawny pesel")
        self.assertEqual(response_data["nazwisko"], account["nazwisko"], "Niepoprawne nazwisko")

    @parameterized.expand([
        ("test_usuniecie_account_dobrze", "12345678901", 200),
        ("test_usuniecie_account_zle", "00000000000", 404)
    ])
    def test_usunecie(self, name, pesel, expected_kod):
        print(f"Test: {name}")
        response = requests.delete(f"{self.BASE_URL}/{pesel}")
        self.assertEqual(response.status_code, expected_kod, "Niepoprawny kod błędu")

    def test_wyczysc_rejestr(self):
        data = {
            "imie": "Marek",
            "nazwisko": "Nowak",
            "pesel": "23456789012"
        }
        response = requests.post(f"{self.BASE_URL}", json=data)
        self.assertEqual(response.status_code, 201, "Niepoprawny kod błędu przy tworzeniu konta")

        response = requests.get(f"{self.BASE_URL}/count")
        self.assertTrue(response.json()["count"] > 0, "Rejestr nie zawiera konta przed czyszczeniem")

        response = requests.post(f"{self.BASE_URL}/clear")
        self.assertEqual(response.status_code, 200, "Niepoprawny kod błędu przy czyszczeniu rejestru")

        response = requests.get(f"{self.BASE_URL}/count")
        self.assertEqual(response.json()["count"], 0, "Rejestr nie został wyczyszczony")

    def test_backup_danych(self):
        response = requests.post(f"{self.BASE_URL}/backup", json={"filepath": f"../{self.backup_filepath}"})
        self.assertEqual(response.status_code, 200, "Niepoprawny kod błędu przy zapisywaniu backupu")


        self.assertTrue(os.path.exists(f"{self.backup_filepath}"), "Plik backupu nie został utworzony")

        with open(f"{self.backup_filepath}", 'r') as file:
            dane = json.load(file)
            self.assertGreater(len(dane), 0, "Brak danych w pliku backupu!")



    def test_restore_danych(self):
        response = requests.post(f"{self.BASE_URL}/restore", json={"filepath": f"../{self.backup_filepath}"})
        self.assertEqual(response.status_code, 200, "Niepoprawny kod błędu przy zapisywaniu backupu")

        # Usuwamy konto
        pesel = self.account_data["pesel"]
        requests.delete(f"{self.BASE_URL}/{pesel}")

        # Przywracanie danych z backupu
        response = requests.post(f"{self.BASE_URL}/restore", json={"filepath": f"../{self.backup_filepath}"})
        self.assertEqual(response.status_code, 200, "Niepoprawny kod błędu przy przywracaniu danych")

        # Sprawdzamy, czy konto zostało przywrócone
        restored_account = requests.get(f"{self.BASE_URL}/{pesel}").json()
        self.assertEqual(restored_account["pesel"], self.account_data["pesel"], "Niepoprawny pesel po przywróceniu")
        self.assertEqual(restored_account["imie"], self.account_data["imie"], "Niepoprawne imie po przywróceniu")
        self.assertEqual(restored_account["nazwisko"], self.account_data["nazwisko"],"Niepoprawne nazwisko po przywróceniu")

