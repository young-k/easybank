from twilio.rest import TwilioRestClient

account_sid = "ACdb871b2df01671e003111fbc751b75a2"
auth_token = "96c561e908a9c0d97c2a4bf1380332f0"

def send_message(message):
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(to="+13477579097", from_="+16467988051",
                                     body=message)

if __name__ == "__main__":
    send_message("This is a sample message.")
    pass