import json
from .PersonalAccount import  PersonalAccount
class AccountsRegistry:
    rejestry = []

    @classmethod
    def dodaj_account(cls, account):
        pes = account.pesel
        if len(account.pesel) == 11 and all(x.pesel != pes for x in cls.rejestry):
            cls.rejestry.append(account)

    @classmethod
    def policz_accounts(cls):
        return len(cls.rejestry)

    @classmethod
    def znajdz_account_po_peselu(cls, pesel):
        for konto in cls.rejestry:
            if konto.pesel == pesel:
                return konto
        return None

    @classmethod
    def usun_account_po_peselu(cls, pesel):
        konto = cls.znajdz_account_po_peselu(pesel)
        if konto:
            cls.rejestry.remove(konto)
            return True
        return False

    @classmethod
    def wyczysc_rejestr(cls):
        cls.rejestry.clear()


    @classmethod
    def zrzuc_dane_do_pliku(cls, filepath):
        zawartosc = []
        for account in cls.rejestry:
            zawartosc.append({
            "imie": account.imie,
            "nazwisko": account.nazwisko,
            "pesel": account.pesel,
        })
        with open(filepath, 'w') as file:
            json.dump(zawartosc, file, indent=4)

    @classmethod
    def zaladuj_dane_z_pliku(cls, filepath):
        cls.wyczysc_rejestr()
        with open(filepath, 'r') as file:
            dane = json.load(file)
            for account_data in dane:
                print(account_data)
                account = PersonalAccount(
                    account_data['imie'],
                    account_data['nazwisko'],
                    account_data['pesel'],
                )
                cls.dodaj_account(account)



