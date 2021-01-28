from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=30)
    email = models.EmailField(max_length=35, unique=True)
    cell_number = models.IntegerField()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    objects = UserManager()

