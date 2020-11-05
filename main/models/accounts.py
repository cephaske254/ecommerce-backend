from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission, AbstractUser
from django.utils.translation import gettext_lazy as _
from main.utils import accounts
import random, string
from main.utils import verification_token


class User(AbstractUser):
    objects = accounts.UserManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.email:
            self.__original_email = self.email

    def generate_user_id(self):
        random_id = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        while User.objects.filter(pk=random_id).exists():
            random_id = "".join(random.choices(string.ascii_letters, k=8))
        return random_id

    __original_email = None
    username = None
    id = models.CharField(
        max_length=200,
        primary_key=True,
        editable=False,
        unique=True,
    )
    full_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=40, unique=True)

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    email_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_user_id()
        if self.email:
            self.email = self.email.lower()
        if self.full_name:
            self.full_name = self.full_name.title()
        if str(self.__original_email) != str(self.email):
            self.email_verified = False
            verification_token.SendEmailVerification.send_email(
                user=User.objects.filter(pk=self.pk).first()
            )
        super().save(*args, **kwargs)

    @property
    def first_name(self):
        try:
            return self.full_name.split(" ")[0]
        except:
            return None

    @property
    def last_name(self):
        try:
            full_name = self.full_name.split(" ")
            del full_name[0]
            return " ".join(full_name)
        except:
            return None
