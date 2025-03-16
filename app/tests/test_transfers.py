import unittest
from parameterized import parameterized
from unittest.mock import patch

from ..PersonalAccount import PersonalAccount
from ..CompanyAccount import CompanyAccount

class Przelewy_Personal(unittest.TestCase):
    imie = "Dariusz"
    nazwisko = "Januszewski"
    pesel = "12345678901"

    def setUp(self):
        self.konto = PersonalAccount(self.imie, self.nazwisko, self.pesel)

    @parameterized.expand([
        ("test_przelew_wychodzacy_saldo_wystarczajace", 50, 25, 25),
        ("test_przelew_wychodzacy_saldo_niewystarczajace", 50, 100, 50),
    ])
    def test_pzelew_wychodzacy(self, name, sum, amount, expected):
        print(f"Test: {name}")
        self.konto.saldo = sum
        self.konto.przelew_wychodzacy(amount)
        self.assertEqual(self.konto.saldo, expected, "Po nie udanym przelewie saldo na koncie nie powinno zostać zaktualizowane!")

    def test_przelew_wchodzacy(self):
        self.konto.przelew_wchodzacy(25)
        self.assertEqual(self.konto.saldo, 25, "Po udanym przelewie saldo na koncie powinno zostać zaktualizowane!")

    def test_seria_przelewow(self):
        self.konto.saldo = 50
        self.konto.przelew_wchodzacy(25)
        self.konto.przelew_wychodzacy(50)
        self.konto.przelew_wchodzacy(25)
        self.assertEqual(self.konto.saldo, 50, "Po udanym przelewie saldo na koncie powinno zostać zaktualizowane!")

    @parameterized.expand([
        ("test_przelew_ekspresowy_wychodzacy_saldo_wystarczajace", 50, 25, 50-25-1),
        ("test_przelew_ekspresowy_wychodzacy_saldo_niewystarczajace", 50, 100, 50),
        ("test_przelew_ekspresowy_wychodzacy_ponizej_zera", 50, 50, 50-50-1)
    ])
    def test_pzelew_ekspresowy_wychodzacy(self, name, sum, amount, expected):
        print(f"Test: {name}")
        self.konto.saldo = sum
        self.konto.przelew_ekspresowy_wychodzacy(amount)
        self.assertEqual(self.konto.saldo, expected,"Po nie udanym przelewie saldo na koncie nie powinno zostać zaktualizowane!")


    def test_historia(self):
        self.konto.saldo = 50
        self.konto.przelew_wchodzacy(25)
        self.konto.przelew_wychodzacy(50)
        self.konto.przelew_wchodzacy(25)
        self.konto.przelew_ekspresowy_wychodzacy(5)
        self.assertEqual(self.konto.historia, [25, -50, 25, -5, -1], "Po udanym przelewie saldo na koncie powinno zostać zaktualizowane!")


class Przelewy_Company(unittest.TestCase):
    imie = "AAA"
    nip = "8461627563"

    @patch('app.CompanyAccount.CompanyAccount.sprawdz_nip')
    def setUp(self, mock_request):
        mock_request.return_value = True

        self.konto = CompanyAccount(self.imie, self.nip)

    @parameterized.expand([
        ("test_przelew_wychodzacy_saldo_wystarczajace", 50, 25, 25),
        ("test_przelew_wychodzacy_saldo_niewystarczajace", 50, 100, 50),
    ])
    def test_pzelew_wychodzacy(self, name, sum, amount, expected):
        print(f"Test: {name}")
        self.konto.saldo = sum
        self.konto.przelew_wychodzacy(amount)
        self.assertEqual(self.konto.saldo, expected, "Po nie udanym przelewie saldo na koncie nie powinno zostać zaktualizowane!")

    def test_przelew_wchodzacy(self):
        self.konto.przelew_wchodzacy(25)
        self.assertEqual(self.konto.saldo, 25, "Po udanym przelewie saldo na koncie powinno zostać zaktualizowane!")

    def test_seria_przelewow(self):
        self.konto.saldo = 50
        self.konto.przelew_wchodzacy(25)
        self.konto.przelew_wychodzacy(50)
        self.konto.przelew_wchodzacy(25)
        self.assertEqual(self.konto.saldo, 50, "Po udanym przelewie saldo na koncie powinno zostać zaktualizowane!")

    @parameterized.expand([
        ("test_przelew_ekspresowy_wychodzacy_saldo_wystarczajace", 50, 25, 50 - 25 - 5),
        ("test_przelew_ekspresowy_wychodzacy_saldo_niewystarczajace", 50, 100, 50),
        ("test_przelew_ekspresowy_wychodzacy_ponizej_zera", 50, 50, 50 - 50 - 5)
    ])


    def test_pzelew_ekspresowy_wychodzacy(self, name, sum, amount, expected):
        print(f"Test: {name}")
        self.konto.saldo = sum
        self.konto.przelew_ekspresowy_wychodzacy(amount)
        self.assertEqual(self.konto.saldo, expected,"Po nie udanym przelewie saldo na koncie nie powinno zostać zaktualizowane!")

    def test_historia(self):
        self.konto.saldo = 50
        self.konto.przelew_wchodzacy(25)
        self.konto.przelew_wychodzacy(50)
        self.konto.przelew_wchodzacy(25)
        self.konto.przelew_ekspresowy_wychodzacy(5)
        self.assertEqual(self.konto.historia, [25, -50, 25, -5, -5], "Po udanym przelewie saldo na koncie powinno zostać zaktualizowane!")
