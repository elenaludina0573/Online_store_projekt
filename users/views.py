import random
import secrets
import string

from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterFrom, UserProfileFrom
from users.models import User


class UserLogin(LoginView):
    template_name = 'users/login.html'


class UserLogout(LogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterFrom
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.set_password(user.password)
        verification_code = secrets.token_hex(16)
        user.verification_code = verification_code
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{verification_code}'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, переди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, verification_code):
    user = get_object_or_404(User, verification_code=verification_code)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class ResetPassword(TemplateView):
    def get(self, request):
        return render(request, 'users/reset.html')

    def post(self, request):
        mail = request.POST.get('mail')
        user = get_object_or_404(User, email=mail)
        letters = list(string.ascii_lowercase)
        new_password = ''
        for i in range(8):
            new_password = new_password + random.choice(letters) + str(random.randint(1, 9))
            user.set_password(new_password)
        user.save()
        message = (f'Ваш новый пароль: {new_password}'
                   f'Сохраняйте в тайне!')
        send_mail(
            subject='Новый пароль',
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return redirect('users:login')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileFrom
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

