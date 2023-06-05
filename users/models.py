from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

from users.validators import username_validator


GENDER_MALE = 0
GENDER_FEMALE = 1
GENDER_CHOICES = [
    (GENDER_MALE, 'Male'),
    (GENDER_FEMALE, 'Female')
]


class CustomUserManager(BaseUserManager):
    error_message = {
        "username_exists": "A user with that username already exists.",
        "email_exists": "A user with that email already exists.",
        "password_mismatch": "The password doesn't match.",
        "password_too_short": "Password is too short. Minimum 8 characters.",
        "invalid_value": "Invalid value."
    }
    MINIMUM_PASSWORD_CHAR_LENGTH = 8

    def create_superuser(self, username, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('full_name', 'Superuser')
        other_fields.setdefault('date_of_birth', '2000-01-01')
        other_fields.setdefault('gender', 0)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')

        return self.create_user(username, email, password, password, **other_fields)

    def create_user(self, username, email, gender, password, password2, **other_fields):
        username = username.lower()

        email = self.normalize_email(email)

        user = self.model(username=username, email=email, gender=gender, password=password, **other_fields)

        self.validate_username(username)
        self.validate_email(email)
        self.validate_gender(gender)
        self.validate_password(user, password2)

        user.set_password(password)
        user.save()
        return user

    def validate_username(self, username):
        err_code = "username_exists"
        if self.model.objects.filter(username=username).exists():
            raise ValidationError(message={
                "username": self.error_message[err_code]
            }, code=err_code)

    def validate_email(self, email):
        err_code = "email_exists"
        if self.model.objects.filter(email=email).exists():
            raise ValidationError(message={
                "email": self.error_message[err_code]
            }, code=err_code)

    def validate_gender(self, gender):
        err_code = "invalid_value"
        try:
            GENDER_CHOICES[gender]
        except IndexError:
            raise ValidationError(message={
                "gender": self.error_message[err_code]
            }, code=err_code)

    def validate_password(self, user_instance, password2):
        password = user_instance.password

        if len(password) < self.MINIMUM_PASSWORD_CHAR_LENGTH:
            err_code = "password_too_short"
            raise ValidationError(message={
                "password": self.error_message[err_code]
            }, code=err_code)

        if password != password2:
            err_code = "password_mismatch"
            raise ValidationError(message={
                "password": self.error_message[err_code]
            }, code=err_code)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True, validators=[username_validator], error_messages={
            'unique': "A user with that username already exists.",
        })
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
