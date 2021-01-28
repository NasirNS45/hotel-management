from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models


# Create your models here.
class Admin(AbstractBaseUser, PermissionsMixin):
    default_image_path = 'images/default_profile_picture.jpg'

    full_name = models.CharField(max_length=50)
    email = models.EmailField(_('email address'), unique=True)
    profile_picture = models.ImageField(upload_to='user_images', null=True, blank=True,
                                        default_image_path=default_image_path)
    phone = models.CharField(max_length=20, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    username = models.CharField(max_length=100, null=True, blank=True, unique=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return '{} / {}'.format(self.full_name, self.email)
