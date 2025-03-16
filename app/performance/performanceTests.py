import unittest
import requests


class PerfTest(unittest.TestCase):
    body = {
        "imie": "Dariusz",
        "nazwisko": "Januszewski",
        "pesel": "12345678901"
    }
    BASE_URL = "http://127.0.0.1:5000/api/accounts"
    iteration_count = 100
    timeout = 0.5

    # Test 1: Tworzenie i usuwanie 100 kont
    def test_tworzenie_i_usuniecie(self):
        for i in range(self.iteration_count):
            create_response = requests.post(self.BASE_URL, json=self.body, timeout=self.timeout)
            self.assertEqual(create_response.status_code, 201)
            delete_response = requests.delete(f"{self.BASE_URL}/{self.body['pesel']}", timeout=self.timeout)
            self.assertEqual(delete_response.status_code, 200)

    # Test 2: Tworzenie konta i księgowanie 100 przelewów
    def test_tworzenie_i_przelew(self):
        create_response = requests.post(self.BASE_URL, json=self.body, timeout=self.timeout)
        self.assertEqual(create_response.status_code, 201)
        for i in range(self.iteration_count):
            transfer_response = requests.post(f"{self.BASE_URL}/{self.body['pesel']}/transfer", json ={ "type": "incoming", "amount": 100},timeout=self.timeout )
            self.assertEqual(transfer_response.status_code, 200)
        account = requests.get(f"{self.BASE_URL}/{self.body['pesel']}", timeout=self.timeout)
        self.assertEqual(account.json()['saldo'], 100*self.iteration_count)
        delete_response = requests.delete(f"{self.BASE_URL}/{self.body['pesel']}", timeout=self.timeout)
        self.assertEqual(delete_response.status_code, 200)
