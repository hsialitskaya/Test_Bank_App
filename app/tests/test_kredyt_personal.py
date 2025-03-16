import unittest
from unittest.mock import patch
from parameterized import parameterized

from ..PersonalAccount import PersonalAccount

class Kredyty_Personal(unittest.TestCase):
    imie = "Dariusz"
    nazwisko = "Januszewski"
    pesel = "12345678901"

    def setUp(self):
        self.konto = PersonalAccount(self.imie, self.nazwisko, self.pesel)

    @parameterized.expand([
        ("test_wplaty_suma_weksza", [10, 10, 10, 10, 10], 5, True, 5),
        ("test_wplaty_suma_mniejsza", [1, 1, 1, 1, 1], 10, True, 10),
        ("test_nie_wplaty_suma_wieksza", [5, 2, 3, 3, -1], 10, True, 10),
        ("test_nie_wplaty_suma_mniejsza", [-10, -5, -3, 10, -1], 10, False, 0),
        ("test_pusta_historia", [], 10, False, 0),
        ("test_3_transakcje_dobrze", [10, 20, 30], 10, True, 10),
        ("test_3_transakcje_zle", [10, 20, -30], 10, False, 0)
    ])
    @patch("app.BlackList.BlackList.is_account_on_black_list")
    def test_kredyt(self, name, history, loan, expected_return, expected,  mock_is_account_blocked):
        mock_is_account_blocked.return_value = False
        print(f"Test: {name}")
        self.konto.historia = history
        czy_przyznany = self.konto.zaciagnij_kredyt(loan)
        self.assertEqual(czy_przyznany, expected_return)
        self.assertEqual(self.konto.saldo, expected, "Po nie udanym kredycie saldo na koncie nie powinno zostać zaktualizowane!")

    @patch("app.BlackList.BlackList.is_account_on_black_list")
    def test_kredyt_zablokowany(self, mock_is_account_blocked):
        mock_is_account_blocked.return_value = True
        self.konto.historia = [100, 100, 100]
        self.assertFalse(self.konto.zaciagnij_kredyt(100))

