from .Konto import Konto
from .BlackList import BlackList
black_list_connection = BlackList()

class PersonalAccount(Konto):
    historia = []
    oplata_za_przelew = 1
    email_text = "Twoja historia konta to: "

    def __init__(self, name, surname, pesel, kod_promocyjny=None):
        self.imie = name
        self.nazwisko = surname
        if len(pesel) == 11:
            self.pesel = pesel
        else:
            self.pesel = "Niepoprawny pesel!"

        if self.czy_uprawniony_do_promocji(pesel, kod_promocyjny):
            self.saldo = 50
        else:
            self.saldo = 0


    def poprawnosc_kodu_promocyjnego(self, kod_prom):
        if kod_prom is None:
            return False
        if kod_prom.startswith("PROM_") and len(kod_prom) == 8:
            return True
        else:
            return False

    def czy_uprawniony_do_promocji(self, pesel, kod_prom):
        rok_urodzenia = int(pesel[:2])
        miesiac = int(pesel[2:4])
        if (rok_urodzenia >= 61 and (miesiac >= 1 and miesiac <= 32)) or (
                rok_urodzenia <= 24 and (miesiac >= 1 and miesiac <= 32)):
            if self.poprawnosc_kodu_promocyjnego(kod_prom):
                return True
            else:
                return False
        else:
            return False


    def udzielenie_kredytu(self, kwota):
        if len(self.historia) >= 3:
            if all(x > 0 for x in self.historia[-3:]) or sum(self.historia[-5:]) > kwota:
                return True
            return False
        return False

    def zaciagnij_kredyt(self, kwota):
        if black_list_connection.is_account_on_black_list(self.pesel):
            return False
        if self.udzielenie_kredytu(kwota):
            self.saldo += kwota
            return True
        return False


