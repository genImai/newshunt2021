from functools import reduce
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import User
from newsapp.models import Setting
from django.contrib.auth import login, logout

#ゲストログイン・ログアウト
def guest_login(request):
    guest_user = User.objects.get(email = 'guest@newshunt2021.com')
    login (request,guest_user,backend='django.contrib.auth.backends.ModelBackend')
    return redirect('index')

def guest_logout(request):
    Setting.objects.filter(id='75645299-731b-44a5-8fb7-675ffbeaeb2f').delete()
    logout(request)
    return redirect('account_login')