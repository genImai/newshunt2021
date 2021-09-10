from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User

# Register your models here.

#ユーザーの作成フォーム定義
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput
    )
    

    class Meta:
        model = User
        fields = ('email', 'sex', 'age')
        

    #上のpassword1とpassword2が合致しているか確認
    def clean_password2(self):
        
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("パスワードが合致しません")
        return password2


    #パスワードをハッシュ化して保存
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
#ユーザーの更新フォーム定義
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = ('email', 'password','sex', 'age', \
        'is_active', 'is_admin')
        
    def clean_password(self):
        return self.initial["password"]


#Adminの入力フォーム
class UserAdmin(BaseUserAdmin):
    #上で定義したフォームクラスでインスタンス化
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ('email', 'sex', 'age', 'is_admin')
    list_filter = ('is_admin',)
    #フィールドを作成
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('sex', 'age',)}),
        ('Permissins', {'fields': ('is_admin',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','sex', 'age', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    
admin.site.register(User,UserAdmin)
admin.site.unregister(Group)
