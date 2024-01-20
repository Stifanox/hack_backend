import json


class GPTMessage:

    def __init__(self, messageToCheck):
        self.messageToCheck = messageToCheck

    def getMessage(self):
        return json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [{
                "role": "system",
                "content": f"Oceń czy ta wiadomość jest ofensywna i czy zachęca do złych zachowań: '{self.messageToCheck}'. Jako odpowiedź zwróć JSONa z dwoma kluczami 'value' oraz 'message'. Do value wstaw 1 jeżeli odpowiedź jest ofensywna bądź 0 jeżeli odpowiedź nie jest ofensywna. Do message wstaw wiadomość źródłową "
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
