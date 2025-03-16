import unittest
from unittest.mock import MagicMock, patch
from ..BlackList import BlackList


class TestBlackList(unittest.TestCase):
    pesel = "12345678901"
    reason = "Fraud"
    @patch("pymongo.MongoClient")
    def setUp(self, mock_mongo_client):
        self.mock_client = MagicMock()
        mock_mongo_client.return_value = self.mock_client
        self.black_list_connection = BlackList()

    def tearDown(self):
        self.black_list_connection.close()

    @patch("pymongo.collection.Collection.insert_one")
    def test_dodanie_account_do_black_list(self, mock_insert_one):
        mock_insert_one.return_value.inserted_id = "mock_id"
        self.black_list_connection.add_account_to_black_list(self.pesel, self.reason)
        mock_insert_one.assert_called_once_with({"pesel": self.pesel, "reason": self.reason})

    @patch("pymongo.collection.Collection.find_one")
    def test_czy_account_jest_na_black_list(self, mock_find_one):
        mock_find_one.return_value = {"pesel": self.pesel, "reason": self.reason}
        result = self.black_list_connection.is_account_on_black_list(self.pesel)
        self.assertTrue(result)
        mock_find_one.assert_called_once_with({"pesel": self.pesel})

        mock_find_one.return_value = None
        result = self.black_list_connection.is_account_on_black_list("102938475610")
        self.assertFalse(result)
        mock_find_one.assert_called_with({"pesel": "102938475610"})

        self.black_list_connection.close()