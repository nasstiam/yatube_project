# users/views.py
# Импортируем CreateView, чтобы создать ему наследника
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordChangeDoneView, \
    PasswordResetDoneView
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.core.mail import send_mail

# Функция reverse_lazy позволяет получить URL по параметрам функции path()
# Берём, тоже пригодится
from django.urls import reverse_lazy

# Импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm, AuthenticationForm, SetPasswordForm


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
    # send_mail('Yatube password reset', 'resetresetreset', 'nasstiam@yandex.ru', ['nasstiam@yandex.ru'], fail_silently=False)
    form_class = PasswordResetForm
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')


class PasswordChangeDone(PasswordChangeDoneView):
    form_class = PasswordChangeForm
    template_name = 'users/password_change_done.html'


class PasswordResetDone(PasswordResetDoneView):
    form_class = PasswordResetForm
    template_name = 'users/password_reset_done.html'


# def password_change(request):
#     user = request.user
#     print(request.method)
#     if request.method == 'POST':
#         form = SetPasswordForm(user, request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#                 return redirect('users:password_change_done')
#             except Exception as e:
#                 form.add_error(None, 'Ошибка смены пароля')
#     else:
#         form = SetPasswordForm(user)
#     return render(request, 'users/password_change.html', {'form': form})

