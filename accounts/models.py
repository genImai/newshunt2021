from django.db import models
from django.contrib.auth.models import(
    BaseUserManager,AbstractBaseUser, PermissionsMixin
)
import uuid

class UserManager(BaseUserManager):
    #一般ユーザーの作成
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('メールアドレスは必須です')
        
        user = self.model(
            email=self.normalize_email(email),
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    #スーパーユーザーの作成
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
    
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='メールアドレス',
        max_length=255,
        unique=True,
    )
    sex = models.CharField(verbose_name='性別',max_length=10)
    age = models.CharField(verbose_name='年齢',blank=True,max_length=10)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
    



