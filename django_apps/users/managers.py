from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        """Validates that the provided email is in the correct format."""
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address."))

    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        """Create and return a regular user with the provided details."""
        if not first_name:
            raise ValueError(_("Users must have a first name."))
        if not last_name:
            raise ValueError(_("Users must have a last name."))
        if not email:
            raise ValueError(_("Users must have an email address."))

        email = self.normalize_email(email)
        self.email_validator(email)

        # Set default values for is_staff and is_superuser if not provided
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        # Create and save the user
        user = self.model(
            first_name=first_name, last_name=last_name, email=email, **extra_fields
        )
        
        # Ensure password is set properly
        if password:
            user.set_password(password)
        else:
            raise ValueError(_("The password is required."))
        
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password=None, **extra_fields):
        """Create and return a superuser with the provided details."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        if not password:
            raise ValueError(_("Superuser must have a password."))

        return self.create_user(first_name, last_name, email, password, **extra_fields)
