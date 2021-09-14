from django import forms
from .models import Setting



class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = ('key1', 'key2', 'key3',\
            'site1', 'site2', 'site3', 'site4','site5',)
        
        
        labels = {
            'key1': 'キーワード1',
            'key2': 'キーワード2',
            'key3': 'キーワード3',
            'site1': 'yahoo!ニュース',
            'site2': '日経電子版',
            'site3': '株探（材料）',
            'site4': '株探（決算）',
            'site5': '時事ドットコム',
        }
        widgets = {
            'site1': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'site2': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'site3': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'site4': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'site5': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }
        
    def clean(self):
        cleaned_data = super(SettingForm, self).clean()
        site1 = self.cleaned_data.get('site1')
        site2 = self.cleaned_data.get('site2')
        site3 = self.cleaned_data.get('site3')
        site4 = self.cleaned_data.get('site4')
        site5 = self.cleaned_data.get('site5')
        if site1==False and site2==False and site3==False and site4==False and site5==False:
            raise forms.ValidationError("検索対象サイトを最低１つ選択してください。")
        return cleaned_data