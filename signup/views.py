from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib import messages
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import auth

from HMS import settings
from .forms import SignUpForm


# Create your views here.
from .models import CustomUser
from .token import account_activation_token


class WelcomeView(View):

    def get(self, request):
        user = request.user
        return render(request, 'base.html', {'name': user})


class SignUpView(View):

    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            subject = 'Account Activation.'
            current_site = get_current_site(request)
            uid = user.id
            token = account_activation_token.make_token(user)
            activation_link = "http://{0}/accounts/activate/{1}/{2}".format(current_site, uid, token)
            from_email = settings.EMAIL_HOST_USER
            to_email = [form.cleaned_data.get('email'), ]
            context = {'activation_link': activation_link}
            message = "Visit {}  to activate your account".format(activation_link)
            mail.send_mail(subject, message, from_email, to_email, context)
            return redirect('accounts:confirm_email', uid=uid, token=token, check=0)
        else:
            return render(request, 'signup/signup.html', {'form': form})


class ConfirmEmail(View):

    def get(self, request, uid, token, check):
        if request.user.is_authenticated:
            return redirect('/')

        new_user = CustomUser.objects.get(pk=uid)
        template = 'signup/confirm-email.html'
        context = {'user': new_user, 'uid': uid, 'token': self.kwargs['token'], 'subject': 'Account Activation'}
        return render(request, template, context)


class Activate(View):

    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(self.kwargs['uid']))
            user = CustomUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, self.kwargs['token']):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return render_to_response('signup/invalid_link.html')