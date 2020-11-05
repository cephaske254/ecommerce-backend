import six, threading
from threading import Thread
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from datetime import timezone, datetime


class TokenGenerator(PasswordResetTokenGenerator):
    algorithm='sha1'

account_activation_token = TokenGenerator()

class SendEmailVerification(TokenGenerator, Thread):
    def __init__(self, user, subject="Verify Your Email"):
        self.user = user
        self.subject = subject
        self.recipient_list = [user.email]
        token = self.make_token(user=user)
        print(token)
        self.html_content = render_to_string(
            "accounts/email_verification.html",
            context={
                "user": self.user,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": token,
                "domain": "localhost:8000",
                "site_title": "e-Commerce"
            },
        )
        threading.Thread.__init__(self)

    def send_email(user, subject="Verify Your Email"):
        SendEmailVerification(user, subject).start()

    def run(self):
        html_message = strip_tags(self.html_content)
        msg = EmailMultiAlternatives(
            self.subject,
            html_message,
            to=self.recipient_list,
            headers={"X-Priority": 1},
        )
        msg.attach_alternative(self.html_content, "text/html")
        msg.content_subtype = "html"
        msg.send(fail_silently=True)