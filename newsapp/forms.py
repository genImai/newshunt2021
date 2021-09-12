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