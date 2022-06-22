import jwt
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from enum import Enum

import datetime


AUTH_PROVIDERS = (
                     ('google.com', 'google'),
                     ('email', 'email'),
)


# Create your models here.
class UserManager(BaseUserManager):
    """
    Custom Manager class which inherits 'BaseUserManager', we will override the 'create_user' and 'create_superuser'
    functions in order to use it to create regular 'User' objects and super-users (admins) respectively
    """

    def create_user(self, email, username, auth_provider, is_active=True, password=None):
        """
            Creates and saves a new regular user.
        """
        if not email:
            raise ValueError('Users must have an email address.')
        if not username:
            raise ValueError('Users must have an username.')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            auth_provider=auth_provider,
            is_active=is_active
        )

        user.set_password(password)
        user.save(self._db)

        return user

    def create_superuser(self, email, username, password):
        """
            Creates and saves a new superuser.
        """
        if not email:
            raise ValueError('Users must have an email address.')
        if not username:
            raise ValueError('Users must have an username.')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
        )
        user.set_password(password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True

        user.save(self._db)

        return user


class User(PermissionsMixin, AbstractBaseUser):
    """
        Defines the custom user class that our system will use.
    """
    username = models.CharField(max_length=255)
    email = models.EmailField(validators=[validators.validate_email], unique=True, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    auth_provider = models.CharField(max_length=255, blank=False, null=False, choices=AUTH_PROVIDERS, default='email')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
            This method is required by Django for things like handling emails.
            Typically this would be the user's first and last name. in our case,
            we return their username.
        """
        return self.username

    def get_short_name(self):
        """
            This method is required by Django for things like handling emails.
            Typically this would be the user's first name. in our case,
            we return their username.
        """
        return self.username

    def _generate_jwt_token(self):
        """
            Generates a JSON WEB TOKEN that stores this user's ID and an expiration delay
        """
        dt = datetime.now() + timedelta(days=30)
        token = jwt.encode(
            payload={
                'id': self.pk,
                'exp': int(dt.strftime('%s'))
            },
            key=settings.SECRET_KEY,
            algorithm='HS256'
        )

        return token.decode('utf-8')

    @property
    def token(self):
        """
            Allows us to get user's token by calling 'user.token
            The '@property' decorator above makes this possible
        """
        return self._generate_jwt_token()


class Genders(Enum):
    MALE = 'Male'
    FEMALE = 'Female'


class Profile(models.Model):
    user = models.OneToOneField(
        to='User',
        on_delete=models.CASCADE
    )
    image = models.URLField(default='https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/User_font_awesome.svg/2048px-User_font_awesome.svg.png', max_length=5550)
    full_name = models.CharField(max_length=255, null=False, blank=False)


    def __str__(self):
        return '{}\'s Profile'.format(self.user.username)
