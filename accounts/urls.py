from os import name
from django.urls import path
from .views import guest_login, guest_logout

urlpatterns = [
    path('guest_login/',guest_login, name='account_guest_login'),
    path('guest_logout/',guest_logout, name='account_guest_logout'),
]
