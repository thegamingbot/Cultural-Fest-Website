from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager

# Create your models here.
class user(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_('name'), max_length=64, null=True)
    username = models.CharField(_('username'), max_length=64, unique=True, null=True)
    email = models.EmailField(_('email address'), unique=True, null=True)
    phone = models.IntegerField(_('phone'), null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True)
