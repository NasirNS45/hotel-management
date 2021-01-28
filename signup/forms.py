from django import forms
from django.core.exceptions import ValidationError

from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
import re

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
FULL_NAME_REGEX = r'^[a-zA-Z]+(([,. -][a-zA-Z ])?[a-zA-Z]*)*$'
PHONE_REGEX = r'(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+$'


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = 'form-input'
        self.fields['password2'].widget.attrs['class'] = 'form-input'
        self.fields['fullname'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
        self.fields['cell_number'].widget.attrs['placeholder'] = 'Enter your contact Number'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

    class Meta:
        model = CustomUser
        fields = ['fullname', 'email', 'cell_number', 'password1', 'password2']

    def clean(self):
        return self.cleaned_data

    def clean_full_name(self):
        fullname = self.cleaned_data['full_name']
        is_valid_fullname = re.match(FULL_NAME_REGEX, fullname)
        if not is_valid_fullname or not fullname:
            raise forms.ValidationError('Enter a valid name. Number and special characters are not Allowed.')
        return fullname

    def clean_email(self):
        email = self.cleaned_data['email']
        is_valid_email = re.match(EMAIL_REGEX, email)

        if not is_valid_email or not email:
            raise forms.ValidationError("Email is invalid")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        is_valid_phone = re.match(PHONE_REGEX, phone)
        if not is_valid_phone or not phone:
            raise forms.ValidationError("Phone number is invalid")
        return phone

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise ValidationError("This password must contain at least 8 characters.", code='password_too_short',
                                  params={'min_length': 8}, )
        return password
