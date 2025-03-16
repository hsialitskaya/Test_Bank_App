import unittest
from parameterized import parameterized

from ..PersonalAccount import PersonalAccount

class TestCreatePersonalAccount(unittest.TestCase):
    imie = "Dariusz"
    nazwisko = "Januszewski"
    pesel = "12345678901"

    def test_tworzenie_konta(self):
        pierwsze_konto = PersonalAccount(self.imie, self.nazwisko, self.pesel)
        self.assertEqual(pierwsze_konto.imie, self.imie, "Imie nie zostało zapisane!")
        self.assertEqual(pierwsze_konto.nazwisko, self.nazwisko, "Nazwisko nie zostało zapisane!")

    @parameterized.expand([
        ("test_zakrotki_pesel", "123", "Niepoprawny pesel!"),
        ("test_zadlugi_pesel", "123123123123123123123123", "Niepoprawny pesel!"),
    ])

    def test_pesel(self, name, pesel, expected):
        print(f"Test: {name}")
        konto = PersonalAccount(self.imie, self.nazwisko, pesel)
        self.assertEqual(konto.pesel, expected, "Pesel nie zostal zapisany!")

    @parameterized.expand([
        ("test_dobry_kod_dobry_wiek", "61123478901", "PROM_123", 50),
        ("test_zly_kod_dlugosc_dobry_wiek", "65123478901", "PROM_12", 0),
        ("test_zly_kod_prefix_dobry_wiek", "65123478901", "PROM_1234", 0),
        ("test_dobry_kod_zly_wiek", "49123478901", "PROM_123", 0),
        ("test_zly_kod_zly_wiek", "49123478901", "PRO_123", 0)
    ])

    def test_kod_promocyjny(self, name, pesel, kod, expected):
        print(f"Test: {name}")
        konto = PersonalAccount(self.imie, self.nazwisko, pesel, kod)
        self.assertEqual(konto.saldo, expected, "Zły kod promocyjny!")
        
