import unittest
import json
import os
from parameterized import parameterized

from ..AccountsRegistry import AccountsRegistry
from ..PersonalAccount import PersonalAccount


class TestRegistry(unittest.TestCase):
    imie = "Dariusz"
    nazwisko = "Januszewski"
    pesel = "12345678901"
    pesel_66 = "89092909866"
    pesel_77 = "89092909877"
    filepath = "test_backup.json"

    @classmethod
    def setUpClass(cls):
        cls.konto1 = PersonalAccount(cls.imie, cls.nazwisko, cls.pesel)
        cls.konto2 = PersonalAccount(cls.imie, cls.nazwisko, cls.pesel_66)
        cls.konto3 = PersonalAccount(cls.imie, cls.nazwisko, cls.pesel_77)

    def setUp(self):
        AccountsRegistry.rejestry = []

    def test_dodaj_account_rejestr_pusty(self):
        AccountsRegistry.dodaj_account(self.konto1)
        self.assertEqual(AccountsRegistry.policz_accounts(), 1, "Niepoprawna ilosc kont w rejestrze!")

    def test_dodaj_account_rejestr_nie_pusty(self):
        AccountsRegistry.rejestry = [self.konto1]
        AccountsRegistry.dodaj_account(self.konto2)
        self.assertEqual(AccountsRegistry.policz_accounts(), 2, "Niepoprawna ilosc kont w rejestrze!")

    def test_dodaj_pare_accounts_dobrze(self):
        AccountsRegistry.dodaj_account(self.konto1)
        AccountsRegistry.dodaj_account(self.konto2)
        AccountsRegistry.dodaj_account(self.konto3)
        self.assertEqual(AccountsRegistry.policz_accounts(), 3, "Niepoprawna ilosc kont w rejestrze!")

    def test_dodaj_pare_accounts_zle(self):
        self.konto4 = PersonalAccount(self.imie, self.nazwisko, self.pesel_77)
        AccountsRegistry.dodaj_account(self.konto1)
        AccountsRegistry.dodaj_account(self.konto2)
        AccountsRegistry.dodaj_account(self.konto3)
        AccountsRegistry.dodaj_account(self.konto4)
        self.assertEqual(AccountsRegistry.policz_accounts(), 3, "Niepoprawna ilosc kont w rejestrze!")


    @parameterized.expand([
        ("test_dodaj_account_krotki_pesel", "123"),
        ("test_dodaj_account_dlugi_pesel", "123123123123123"),
    ])
    def test_dodaj_account(self, name, pesel):
        print(f"Test: {name}")
        self.konto4 = PersonalAccount(self.imie, self.nazwisko, pesel)
        AccountsRegistry.dodaj_account(self.konto4)
        self.assertEqual(AccountsRegistry.policz_accounts(), 0, "Niepoprawna ilosc kont w rejestrze!")

    def test_wyszukaj_po_peselu_dobrze(self):
        AccountsRegistry.dodaj_account(self.konto1)
        AccountsRegistry.dodaj_account(self.konto2)
        result = AccountsRegistry.znajdz_account_po_peselu(self.pesel)
        self.assertEqual(result, self.konto1, "Niepoprawne konto znalezione po PESEL!")

    def test_wyszukaj_po_peselu_zle(self):
        AccountsRegistry.dodaj_account(self.konto1)
        result = AccountsRegistry.znajdz_account_po_peselu(self.pesel_66)
        self.assertEqual(result, None, "Niepoprawne konto znalezione po PESEL!")

    def test_wyszukaj_po_peselu_pusty_rejestr(self):
        result = AccountsRegistry.znajdz_account_po_peselu(self.pesel)
        self.assertEqual(result, None, "Niepoprawne konto znalezione po PESEL!")

    def test_wyszukaj_po_peselu_usuniete_konto(self):
        AccountsRegistry.dodaj_account(self.konto1)
        AccountsRegistry.dodaj_account(self.konto2)
        AccountsRegistry.usun_account_po_peselu(self.konto1.pesel)
        result = AccountsRegistry.znajdz_account_po_peselu(self.pesel)
        self.assertEqual(result, None, "Niepoprawne konto znalezione po PESEL!")

    def test_policz_pusty_rejestr(self):
        result = AccountsRegistry.policz_accounts()
        self.assertEqual(result, 0, "Niepoprawna ilosc kont w rejestrze!")

    def test_policz_po_usunieciu(self):
        AccountsRegistry.dodaj_account(self.konto1)
        AccountsRegistry.dodaj_account(self.konto2)
        AccountsRegistry.usun_account_po_peselu(self.konto1.pesel)
        result = AccountsRegistry.policz_accounts()
        self.assertEqual(result, 1, "Niepoprawna ilosc kont w rejestrze!")


    def test_policz_podwujne_dodanie(self):
        AccountsRegistry.dodaj_account(self.konto1)
        AccountsRegistry.dodaj_account(self.konto1)
        result = AccountsRegistry.policz_accounts()
        self.assertEqual(result, 1, "Niepoprawna ilosc kont w rejestrze!")

    def test_policz_po_zmianie_stanu_konta(self):
        AccountsRegistry.dodaj_account(self.konto1)
        self.konto1.saldo = 1000
        result = AccountsRegistry.policz_accounts()
        self.assertEqual(result, 1, "Niepoprawna ilosc kont w rejestrze!")

    @parameterized.expand([
        ("test_usun_konto_po_peselu_dobrze", pesel, 0),
        ("test_usun_konto_po_peselu_zle", pesel_66, 1),
    ])
    def test_usun_konto(self, name, pesel, expected_amount):
        print(f"Test: {name}")
        AccountsRegistry.dodaj_account(self.konto1)
        AccountsRegistry.usun_account_po_peselu(pesel)
        self.assertEqual(AccountsRegistry.policz_accounts(), expected_amount, "Niepoprawna ilosc kont w rejestrze!")

    def test_wyczysc(self):
        AccountsRegistry.dodaj_account(self.konto1)
        AccountsRegistry.dodaj_account(self.konto2)
        AccountsRegistry.dodaj_account(self.konto3)
        AccountsRegistry.wyczysc_rejestr()
        self.assertEqual(AccountsRegistry.policz_accounts(), 0, "Niepoprawna ilosc kont w rejestrze!")

    def test_zrzuc_dane_do_pliku(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

        AccountsRegistry.dodaj_account(self.konto1)
        AccountsRegistry.dodaj_account(self.konto2)

        AccountsRegistry.zrzuc_dane_do_pliku(self.filepath)

        with open(self.filepath, "r") as file:
            dane = json.load(file)

        self.assertEqual(len(dane), 2, "Niepoprawna liczba kont w zapisanym pliku!")

        self.assertEqual(dane[0]["pesel"], self.konto1.pesel, "Niepoprawne dane konta 1 w pliku!")
        self.assertEqual(dane[0]["imie"], self.konto1.imie, "Niepoprawne imię konta 1 w pliku!")
        self.assertEqual(dane[0]["nazwisko"], self.konto1.nazwisko, "Niepoprawne nazwisko konta 1 w pliku!")
        self.assertEqual(dane[1]["pesel"], self.konto2.pesel, "Niepoprawne dane konta 2 w pliku!")
        self.assertEqual(dane[1]["imie"], self.konto2.imie, "Niepoprawne imię konta 2 w pliku!")
        self.assertEqual(dane[1]["nazwisko"], self.konto2.nazwisko, "Niepoprawne nazwisko konta 2 w pliku!")

    def test_zaladuj_dane_z_pliku(self):
        #Tworzenie zawartosci pliku do zaladowania
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

        dane_testowe = [
            {"imie": self.imie, "nazwisko": self.nazwisko, "pesel": self.pesel},
            {"imie": self.imie, "nazwisko": self.nazwisko, "pesel": self.pesel_66},
        ]

        with open(self.filepath, "w") as file:
            json.dump(dane_testowe, file)

        # Przywrócenie danych z pliku i sprawdzenie stanu rejestru
        AccountsRegistry.zaladuj_dane_z_pliku(self.filepath)
        self.assertEqual(AccountsRegistry.policz_accounts(), 2, "Niepoprawna liczba kont po załadowaniu danych!")
        self.assertEqual(AccountsRegistry.znajdz_account_po_peselu(self.pesel).pesel, self.pesel, "Niepoprawne dane konta po załadowaniu!",)
        self.assertEqual(AccountsRegistry.znajdz_account_po_peselu(self.pesel_66).pesel, self.pesel_66, "Niepoprawne dane konta po załadowaniu!",)