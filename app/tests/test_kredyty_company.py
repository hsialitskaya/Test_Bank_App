import unittest
from parameterized import parameterized
from unittest.mock import patch

from ..CompanyAccount import CompanyAccount


class Kredyty_Company(unittest.TestCase):
    imie = "AAA"
    nip = "8461627563"

    @patch('app.CompanyAccount.CompanyAccount.sprawdz_nip')
    def setUp(self, mock_request):
        mock_request.return_value = True
        self.konto = CompanyAccount(self.imie, self.nip)

    @parameterized.expand([
        ("test_dobre_saldo_zus", 500, [10, 10, -1775, 10, 10], 50, 550),
        ("test_zle_saldo_zus", 500, [5, 2, -1775, 3, -1], 500, 500),
        ("test_saldo_dokladnie_2_razy_zus", 500, [10, 10, -1775, 10, 10], 250, 750),
        ("test_saldo_dokladnie_2_razy_nie_zus", 500, [1, 2, 3], 250, 500),
        ("test_dobre_saldo_nie_zus", 500, [1, 1, 1, 1, 1], 50, 500),
        ("test_zle_saldo_nie_zus", 500, [-10, -5, -3, 10, -1], 500, 500),
        ("test_pusta_historia", 500, [], 10, 500)
    ])
    def test_kredyt(self, name, amount, history, loan, expected):
        print(f"Test: {name}")
        self.konto.saldo = amount
        self.konto.historia = history
        self.konto.zaciagnij_kredyt(loan)
        self.assertEqual(self.konto.saldo, expected,
                         "Po nie udanym kredycie saldo na koncie nie powinno zostać zaktualizowane!")
