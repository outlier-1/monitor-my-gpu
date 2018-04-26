from twilio.rest import Client


class SMSAPI:
    def __init__(self):
        self.account_sid = "ACdd5453a78d3fe9fa074d454ef7e0e00d"
        self.auth_token = "5786dbd93a95047b2d285b980b8cc6a5"

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
