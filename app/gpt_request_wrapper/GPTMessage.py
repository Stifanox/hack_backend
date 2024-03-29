import json


class GPTMessage:

    def __init__(self, messageToCheck):
        self.messageToCheck = messageToCheck

    def getCheerMessage(self):
        return json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [{
                "role": "system",
                "content": f"Oceń czy ta wiadomość jest ofensywna i czy zachęca do złych zachowań: '{self.messageToCheck}'. Jako odpowiedź zwróć JSONa z dwoma kluczami 'value' oraz 'message'. Do value wstaw 1 jeżeli odpowiedź jest ofensywna bądź 0 jeżeli odpowiedź nie jest ofensywna. Do message wstaw wiadomość źródłową "
            }]
        })

    def getDailyUpdateMessage(self, uncheered_updates):
        return json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [{
                "role": "system",
                "content": f"Podaje ci wiadomości wysłane cześniej przez użytkownika: '{self.messageToCheck}'. To wiadomości na które użytkownik może odpowiedzieć: '{uncheered_updates}'. Jako odpowiedź zwróć JSONa z numerem wiadomości jako id, na którą użytkownik może odpowiedzieć. Jako id numer z podanej drugiej tablicy, pierwszej nie bierz pod uwagę przy zwracaniu wiadomości."
            }]
        })

    def getMessageForDailyUpdated(self):
        return json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [{
                "role": "system",
                "content": f"Oceń czy ta wiadomość świadczy o bardzo złym samopoczuciu: '{self.messageToCheck}'. W odpowiedzi odeślij JSONa z kluczem isSuspicious którego wartość przyjmuje 1 jeżeli wiadomość wydaje się świadczyć o bardzo złym samopoczuciu lub 0 jeżeli wiadomość nie wydaje się świadczyć o bardzo złym samopoczuciu."
            }]
        })

    def getRecommendedTherapistList(self, psychologistList):
        return json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [{
                "role": "system",
                "content": f"Oto opis problemów pewnego użytkownika: '{self.messageToCheck}'. Tutaj przekazuje ci listę psychologów: {psychologistList}. Wybierz proszę najlepszych trzech i zwróć ich w formie JSONa z kluczem ids, który zawiera tablice id np [1, 2, 3]"
            }]
        })
