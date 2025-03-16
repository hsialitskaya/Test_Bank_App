from .Konto import Konto
import datetime
import requests
import os


class CompanyAccount(Konto):
    historia = []
    oplata_za_przelew = 5
    email_text = "Historia konta Twojej firmy to: "

    def __init__(self, name, nip):
        self.nazwa = name
        if len(nip) == 10:
            if not self.sprawdz_nip(nip):
                raise ValueError(f"NIP {nip} nie istnieje w bazie Ministerstwa Finansów.")
            self.nip = nip
        else:
            print(f"Podany NIP {nip} ma niepoprawną długość, konto zostaje utworzone z oznaczeniem 'Niepoprawny nip'.")
            self.nip = "Niepoprawny nip!"
        self.saldo = 0

    def udzielenie_kredytu(self, kwota):
        if self.saldo >= 2 * kwota and (-1775 in self.historia):
            return True
        return False

    def zaciagnij_kredyt(self, kwota):
        if self.udzielenie_kredytu(kwota):
            self.saldo += kwota

    def sprawdz_nip(self, nip):
        dzisiaj = datetime.datetime.now().strftime('%Y-%m-%d')
        api_url = os.getenv('BANK_APP_MF_URL', 'https://wl-api.mf.gov.pl')
        url = f"{api_url}/api/search/nip/{nip}?date={dzisiaj}"
        print("Wysyłam zapytanie do ", url)
        response = requests.get(url)  # Wysyłamy zapytanie
        if response.status_code == 200:  # Sprawdzamy, czy odpowiedź jest poprawna
            return True
        else:
            return False

