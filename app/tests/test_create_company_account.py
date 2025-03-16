import unittest
from parameterized import parameterized
from unittest.mock import patch
from ..CompanyAccount import CompanyAccount

class TestCreateBankAccount(unittest.TestCase):
    nazwa = "AAA"
    nip = "8461627563"

    @patch('app.CompanyAccount.CompanyAccount.sprawdz_nip')
    def test_tworzenie_konta_firmowego(self, mock_request):
        mock_request.return_value = True

        pierwsze_konto = CompanyAccount(self.nazwa, self.nip)
        self.assertEqual(pierwsze_konto.nazwa, self.nazwa, "Nazwa firmy nie została zapisana!")
        self.assertEqual(pierwsze_konto.nip, self.nip, "Nip firmy nie został zapisany!" )



    @parameterized.expand([
        ("test_zakrotki_nip", "123", "Niepoprawny nip!"),
        ("test_zadlugi_nip", "123123123123123123123123", "Niepoprawny nip!"),
    ])

    @patch('app.CompanyAccount.CompanyAccount.sprawdz_nip')
    def test_nip(self, name, nip, expected, mock_request):
        print(f"Test: {name}")
        mock_request.return_value = False

        konto = CompanyAccount(self.nazwa, nip)
        self.assertEqual(konto.nip, expected, "Nip nie został zapisany!")


    @patch('app.CompanyAccount.CompanyAccount.sprawdz_nip')
    def test_nip_nie_ma_w_bazie(self, mock_request):
        mock_request.return_value = False

        with self.assertRaises(ValueError):
            CompanyAccount(self.nazwa, "0000000000")


    @patch('requests.get')
    def test_sprawdz_nip_good_status_code(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '{"status":"OK"}'
        konto = CompanyAccount(self.nazwa, self.nip)
        self.assertTrue(konto.sprawdz_nip(self.nip))


    @patch('requests.get')
    def test_sprawdz_nip_bad_status_code(self, mock_get):
        mock_get.return_value.status_code = 400
        mock_get.return_value.text = "Bad Request"
        with self.assertRaises(ValueError):
            CompanyAccount(self.nazwa, self.nip).sprawdz_nip(self.nip)



