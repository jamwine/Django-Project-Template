from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email")

    error_messages = {
        "duplicate_email": "A user with this email already exists.",
        "password_mismatch": "The two password fields didn’t match.",
    }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.error_messages["duplicate_email"])
        return email
    
    def clean_password2(self):
        # Ensure passwords match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages["password_mismatch"])
        return password2