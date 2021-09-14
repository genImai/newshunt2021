from django import forms
from allauth.account.forms import SignupForm,ResetPasswordKeyForm
from .models import User



class MyCustomSignupForm(SignupForm):
    CHOICE1 = (
        ('男性','男性'),
        ('女性','女性'),
    )
    CHOICE2 = (
        ('未選択','未選択'),
        ('10代','10代'),
        ('20代','20代'),
        ('30代','30代'),
        ('40代','40代'),
        ('50代','50代'),
        ('60代','60代'),
        ('70代','70代'),
        ('80代','80代'),
        ('90代','90代'),
    )
    
    sex = forms.ChoiceField(label='性別',required=True,widget=forms.RadioSelect(attrs={'class':'form-check form-check-inline', 'id':'id_sex'}),choices=CHOICE1)
    age = forms.ChoiceField(label='年齢',required=True,widget=forms.Select(attrs={'class':'form-select','id':'id_age'}),choices=CHOICE2)
    
    class Meta:
        model = User
        
    def clean_age(self):
        age = self.cleaned_data['age']
        if age == '未選択':
            raise forms.ValidationError("年齢を選択してください")
        return age
    
    
    def clean(self):
        cleaned_data = super(MyCustomSignupForm, self).clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("パスワードが一致しません。")
        return cleaned_data
        

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)
        # Add your own processing here.
        user.sex = self.cleaned_data['sex']
        user.age = self.cleaned_data['age']
        user.save()
        
        # You must return the original result.
        return user
    
class MyCustomResetPasswordKeyForm(ResetPasswordKeyForm):
    
    def clean(self):
        cleaned_data = super(MyCustomResetPasswordKeyForm, self).clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("パスワードが一致しません。")
        return cleaned_data

    def save(self):

        # Add your own processing here.
        # Ensure you call the parent class's save.
        # .save() does not return anything
        super(MyCustomResetPasswordKeyForm, self).save()
    