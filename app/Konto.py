import datetime
from .SMTPClient import SMTPClient

class Konto:
    def przelew_wychodzacy(self, kwota):
        if self.saldo>=kwota:
            self.saldo=self.saldo-kwota
            self.historia.append(-kwota)
            return True
        else:
            self.saldo = self.saldo
            return False

    def przelew_wchodzacy(self, kwota):
        self.saldo=self.saldo+kwota
        self.historia.append(kwota)
        return True

    def przelew_ekspresowy_wychodzacy(self, kwota):
        if self.saldo >= kwota:
            self.saldo = self.saldo - kwota - self.oplata_za_przelew
            self.historia.append(-kwota)
            self.historia.append(-self.oplata_za_przelew)
            return True
        else:
            self.saldo = self.saldo
            return False

    def send_history_to_email(self, email_address):
        smtp_client = SMTPClient()
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        subject = f"Wyciąg z dnia {today_date}"
        text = self.email_text + str(self.historia)
        return smtp_client.send(subject, text, email_address)

