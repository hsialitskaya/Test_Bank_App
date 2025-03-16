import unittest
from ..PersonalAccount import PersonalAccount
from ..CompanyAccount import CompanyAccount
from unittest.mock import patch
import datetime

class TestSendHistoryToEmail(unittest.TestCase):
    email = "email@example.com"

    today = datetime.datetime.now().strftime('%Y-%m-%d')
    email_subject = f'Wyciąg z dnia {today}'

    email_text_personal = "Twoja historia konta to: "
    email_text_company = "Historia konta Twojej firmy to: "

    @patch('app.CompanyAccount.CompanyAccount.sprawdz_nip')
    def setUp(self, mock_request):
        # Tworzenie konta osobistego
        self.personal_account = PersonalAccount("Anna", "Nowak", "12345678901")
        self.personal_account.historia = [100, -1, 500]

        # Tworzenie konta firmowego
        mock_request.return_value = True
        self.company_account = CompanyAccount("Firma XYZ", "8461627563")
        self.company_account.historia = [5000, -1000, 300]

    @patch("app.Konto.SMTPClient.send")
    def test_historia_konto_osobiste(self, send_mock):
        send_mock.return_value = True
        result = self.personal_account.send_history_to_email(self.email)
        self.assertTrue(result)
        send_mock.assert_called_once()

        args, kwargs = send_mock.call_args
        self.assertEqual(args[0], self.email_subject)
        self.assertEqual(args[1], self.email_text_personal + str(self.personal_account.historia))
        self.assertEqual(args[2], self.email)

    @patch("app.Konto.SMTPClient.send")
    def test_historia_konto_firmowe(self, send_mock):
        send_mock.return_value = True
        result = self.company_account.send_history_to_email(self.email)
        self.assertTrue(result)
        send_mock.assert_called_once()

        args, kwargs = send_mock.call_args
        self.assertEqual(args[0], self.email_subject)
        self.assertEqual(args[1], self.email_text_company + str(self.company_account.historia))
        self.assertEqual(args[2], self.email)

    @patch("app.Konto.SMTPClient.send")
    def test_historia_zle_konto_osobiste(self, send_mock):
        send_mock.return_value = False
        result = self.personal_account.send_history_to_email(self.email)
        self.assertFalse(result)
        send_mock.assert_called_once()


    @patch("app.Konto.SMTPClient.send")
    def test_historia_zle_konto_firmowe(self, send_mock):
        send_mock.return_value = False
        result = self.company_account.send_history_to_email(self.email)
        self.assertFalse(result)
        send_mock.assert_called_once()




