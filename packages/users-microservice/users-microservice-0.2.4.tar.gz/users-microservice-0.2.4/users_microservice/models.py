from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """"
    Custom user model to change behaviour of the default user model
    such as validation and required fields.
    """

