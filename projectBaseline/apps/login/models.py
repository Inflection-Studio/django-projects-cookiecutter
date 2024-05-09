import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from .managers import CustomUserManager


# Create your models here.
class UserAccount(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio = models.TextField(verbose_name=_("Bio"), blank=True, null=True)
    history = HistoricalRecords()

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User Account")
        verbose_name_plural = _("User Accounts")
        ordering = ("-date_joined",)
