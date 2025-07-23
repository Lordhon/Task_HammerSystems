from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class User (AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=20, unique=True)
    invite_code = models.CharField(max_length=6, unique=True)
    activated = models.ForeignKey('self' , null=True, blank=True , on_delete=models.SET_NULL)
    code = models.CharField(max_length=4, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.phone_number