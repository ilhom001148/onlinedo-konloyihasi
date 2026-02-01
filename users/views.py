from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings

from .utils import generate_code
from .models import CustomUser, EmailCode
from django.utils import timezone


class RegisterView(View):
    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # if CustomUser.objects.filter(username=username).exists():
        #     return render(request, 'auth/register.html', {
        #         'error': 'Bu username band'
        #     })

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'auth/register.html', {
                'error': 'Bu email allaqachon ishlatilgan'
            })

        if password != confirm_password:
            return render(request, 'auth/register.html', {
                'error': 'Parollar mos emas'
            })

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )

        code = generate_code()

        send_mail(
            "Tasdiqlash kodi",
            f"Sizning tasdiqlash kodingiz: {code}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        EmailCode.objects.create(user=user, code=code)

        request.session['user_id'] = user.id

        return redirect('verify_email')


class Verify_EmailView(View):
    def get(self, request):
        return render(request, 'auth/verify_email.html')

    def post(self, request):
        code = request.POST.get('code')
        user_id = request.session.get('user_id')

        if not user_id:
            return redirect('register')

        otp = EmailCode.objects.filter(user_id=user_id,code=code,is_activated=False).last()

        if not otp:
            return render(request, 'auth/verify_email.html', {
                'error': 'Kod noto‘g‘ri'
            })


        otp.is_activated = True
        otp.save()


        user = otp.user
        user.is_active = True
        user.save()

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'auth/login.html', {
                'error': 'Username yoki parol noto‘g‘ri'
            })

        if not user.is_active:
            return render(request, 'auth/login.html', {
                'error': 'Email tasdiqlanmagan'
            })

        login(request, user)
        return redirect('index')


def logout_(request):
    logout(request)
    return redirect('login')



class Verify_EmailView(View):
    def get(self, request):
        return render(request, 'auth/verify_email.html')

    def post(self, request):
        code = request.POST.get('code')
        user_id = request.session.get('user_id')

        if not user_id:
            return redirect('register')

        otp = EmailCode.objects.filter(
            user_id=user_id,
            code=code,
            is_activated=False
        ).last()


        if not otp:
            return render(request, 'auth/verify_email.html', {
                'error': 'Kod noto‘g‘ri yoki eskirgan'
            })


        if otp.is_expired():
            return render(request, 'auth/verify_email.html', {
                'error': 'Kodning muddati tugagan. Yangi kod so‘rang.'
            })


        otp.is_activated = True
        otp.save()

        user = otp.user
        user.is_active = True
        user.save()

        return redirect('login')





class ResendCodeView(View):
    def get(self, request):
        user_id = request.session.get('user_id')

        if not user_id:
            return redirect('register')

        user = CustomUser.objects.get(id=user_id)

        EmailCode.objects.filter(user=user,is_activated=False).delete()


        EmailCode.objects.filter(user=user, is_activated=False).delete()

        code = generate_code()

        send_mail(
            "Yangi tasdiqlash kodi",
            f"Yangi kodingiz: {code}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        EmailCode.objects.create(user=user, code=code)

        return render(request, 'auth/verify_email.html', {
            'success': 'Yangi kod emailingizga yuborildi'
        })



class HomeView(View):
    login_url = 'login'
    def get(self, request):
        return render(request, 'index.html', {
            'user': request.user
        })