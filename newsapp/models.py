from django.db import models
from accounts.models import User

# Create your models here.


class Setting(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    key1 = models.CharField(max_length=15,blank=False,default='未登録')
    key2 = models.CharField(max_length=15,blank=True,default='未登録')
    key3 = models.CharField(max_length=15,blank=True,default='未登録')
    site1 = models.BooleanField(default=True)
    site2 = models.BooleanField(default=True)
    site3 = models.BooleanField(default=True)
    site4 = models.BooleanField(default=True)
    site5 = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.id) + 'の設定'