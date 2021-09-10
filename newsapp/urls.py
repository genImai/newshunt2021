from .views import SettingCreateView, SettingUpdateView, indexfunc, listfunc, settingConf
from django.urls import path

urlpatterns = [
    path('', indexfunc, name='index'),
    path('list/',listfunc,name='list'),
    path('setting/',settingConf, name='settingConf'),
    path('settingCreate/',SettingCreateView.as_view(), name='create'),
    path('settingUpdate/<uuid:pk>/',SettingUpdateView.as_view(), name='update'),
]