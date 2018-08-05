from twilio.rest import Client


class SMSAPI:
    def __init__(self):
        self.account_sid = "" # Your twilio id
        self.auth_token = "" # Your twilio pw

    Message_Receivers = {
        "Ömer Miraç Baydemir": "+905342021637"
    }

    def send_sms(self, content):
        print("inside send sms function")
        client = Client(self.account_sid, self.auth_token)
        for number in self.Message_Receivers.values():
            print(number)
            message = client.messages.create(
                to=number,
                from_="+18187245816",
                body=content
            )
