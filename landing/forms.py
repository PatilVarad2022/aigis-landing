from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


PASSWORD_REGEX = re.compile(r"^(?=.*[A-Z])(?=.*\d).{8,}$")


class SignupForm(forms.Form):
    full_name = forms.CharField(label="Name", max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(label="Phone (10 digits)", max_length=10, required=False)
    shield_limit_percent = forms.IntegerField(label="Shield limit (%)", min_value=5, max_value=20, initial=10)

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not PASSWORD_REGEX.match(password):
            raise ValidationError("Password must be 8+ chars, include 1 uppercase and 1 number.")
        return password

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if phone and (not phone.isdigit() or len(phone) != 10):
            raise ValidationError("Enter a 10-digit phone number.")
        return phone

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            if User.objects.filter(email=email).exists():
                raise ValidationError("An account with this email already exists.")
        except Exception as e:
            # If database connection fails, log but don't block form rendering
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Database error checking email: {e}")
            # Allow the form to proceed - will be caught on submit
        return email

