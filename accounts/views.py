from functools import reduce
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import User
from newsapp.models import Setting
from django.contrib.auth import login, logout

#ゲストログイン・ログアウト
def guest_login(request):
    guest_user = User.objects.get(email = 'guest@herokuapp.com')
    login (request,guest_user,backend='django.contrib.auth.backends.ModelBackend')
    request.session.set_expiry(30)
    return redirect('index')

def guest_logout(request):
    Setting.objects.filter(id='44b3fa25-5e84-4d7a-8cf2-46185f68c009').delete()
    logout(request)
    return redirect('account_login')
