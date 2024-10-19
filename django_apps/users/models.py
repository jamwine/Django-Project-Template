import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(verbose_name=_("first name"), max_length=50)
    last_name = models.CharField(verbose_name=_("last name"), max_length=50)
    email = models.EmailField(verbose_name=_("email address"), db_index=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # # Custom related_name for groups to avoid reverse accessor conflicts
    # groups = models.ManyToManyField(
    #     Group,
    #     related_name='custom_user_groups',  # Avoiding reverse accessor clash
    #     blank=True,
    #     help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
    #     verbose_name=_('groups')
    # )

    # # Custom related_name for user_permissions to avoid reverse accessor conflicts
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name='custom_user_permissions',  # Avoiding reverse accessor clash
    #     blank=True,
    #     help_text=_('Specific permissions for this user.'),
    #     verbose_name=_('user permissions')
    # )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.first_name

    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def get_short_name(self):
        return self.first_name