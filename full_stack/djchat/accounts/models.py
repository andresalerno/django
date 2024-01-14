from django.contrib.auth.models import AbstractUser
from django.db import models


# abstract user is the starting point to user customization
class Account(AbstractUser):
    pass
