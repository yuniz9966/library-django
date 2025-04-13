from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("ADMIN", "ADMIN"),
        ("MODERATOR", "MODERATOR"),
        ("LIB MEMBER", "LIB MEMBER"),
    ]

    username = models.CharField(max_length=45, unique=True)
    email = models.EmailField(_('email address'), max_length=75, unique=True)
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    role = models.CharField(max_length=35, choices=ROLE_CHOICES, default="LIB MEMBER")
    phone = models.CharField(max_length=45, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    birth_day = models.DateField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email",]

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"


def get_first_admin() -> User:
    return User.objects.filter(role="ADMIN").first().id
