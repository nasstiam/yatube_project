from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordChangeDoneView, \
    PasswordResetDoneView

from django.views.generic import CreateView

from django.urls import reverse_lazy

from .forms import CreationForm, AuthenticationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class LogIn(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('posts:index')


class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:password_change_done')


class PasswordReset(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')


class PasswordChangeDone(PasswordChangeDoneView):
    form_class = PasswordChangeForm
    template_name = 'users/password_change_done.html'


class PasswordResetDone(PasswordResetDoneView):
    form_class = PasswordResetForm
    template_name = 'users/password_reset_done.html'
