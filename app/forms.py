from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from app.models import CustomUser


# class BootstrapAuthenticationForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super(BootstrapAuthenticationForm, self).__init__(*args, **kwargs)
#
#         self.fields['username'].widget.attrs['placeholder'] = 'Email'
#         self.fields['password'].widget.attrs['placeholder'] = 'Password'
#
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'password1']


class LoginForm(forms.Form):
    email = forms.EmailField(label='Enter Email')
    password = forms.CharField(label='Enter Password', widget=forms.PasswordInput)


class RoomBooking(forms.Form):
    checkin = forms.DateField(widget=forms.widgets.DateInput(format="%YYYY/%mm/%dd"), required=True)
    checkout = forms.DateField(widget=forms.widgets.DateInput(format="%YYYY/%mm/%dd"), required=True)
    room = forms.CharField()


class Reservations(forms.Form):
    firstname = forms.CharField(max_length=20)
    middlename = forms.CharField(max_length=20)
    lastname = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=50)
    phone = forms.IntegerField()
    address = forms.CharField(max_length=550)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    zipcode = forms.IntegerField()
    idproof = forms.CharField(max_length=50)
    rooms = forms.IntegerField()


# class SignUpForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(SignUpForm, self).__init__(*args, **kwargs)
#         self.fields['fullname'].widget.attrs['placeholder'] = 'Full Name'
#         self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
#         self.fields['cell_number'].widget.attrs['placeholder'] = 'Enter your contact Number'
#         self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
#         self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
#
#     class Meta:
#         model = CustomUser
#         fields = ['fullname', 'email', 'cell_number', 'password1', 'password2']

