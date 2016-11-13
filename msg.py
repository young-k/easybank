from twilio.rest import TwilioRestClient

account_sid = "AC514060b3911159eb3a64f82778c386d8"
auth_token = "2a7547e5c0424fa28a3f14bf83f3f9b7"

def send_message(message):
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(to="+17328060305", from_="+17322534903 ",
                                     body=message)

