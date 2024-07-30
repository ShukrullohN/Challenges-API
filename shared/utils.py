import threading
import vonage
from django.core.mail import EmailMessage, send_mail
from decouple import config



def send_code_to_email(email, code):
    def send_in_thread():
        import socket
        socket.getaddrinfo('localhost', 8080)
        send_mail(
            from_email=config('EMAIL_HOST'),
            recipient_list=[email],
            subject="Activation code",
            message=f"Your activation code is {code}"
        )

    thread = threading.Thread(target=send_in_thread)
    thread.start()

    return True


def send_code_to_phone(phone_number, code):
    def send_in_thread():
        client = vonage.Client(key=config('VONAGE_KEY'), secret=config('VONAGE_SECRET'))
        sms = vonage.Sms(client)

        responseData = sms.send_message(
    {
        "from": "Vonage APIs",
        "to": phone_number,
        "text": f"Your activation code {code}",
    }
)

        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully.")
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

    thread = threading.Thread(target=send_in_thread)
    thread.start()

    return True
