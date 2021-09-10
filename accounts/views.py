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
    return redirect('index')

def guest_logout(request):
    Setting.objects.filter(id='e24d1eb5-6afa-4f12-b25f-6b8449332446').delete()
    logout(request)
    return redirect('account_login')