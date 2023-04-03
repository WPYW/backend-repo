from django.db import models
from utils.model_abstracts import Model
from django_extensions.db.models import (
	TimeStampedModel, 
	ActivatorModel,
	TitleDescriptionModel
)
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid

# Create your models here.

# 헬퍼 클래스
class UserManager(BaseUserManager):
    # def create_user(self, email, password, nickname, birthday, thumbail_image_url, social, *kwargs):
    def create_user(self, email, password, *kwargs):
        
        """
        주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=email,
            # nickname=nickname,
            # birthday=birthday,
            # thumbail_image_url=thumbail_image_url,
            # social=social
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        """
        주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여
        """
        superuser = self.create_user(
            email=email,
            password=password,
        )
        
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        
        superuser.save(using=self._db)
        return superuser

class Users(
	Model, # PK > 이름 : id, 형식 : uuid
	TimeStampedModel, 
	ActivatorModel,
    AbstractBaseUser,
    PermissionsMixin
	):
    
    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = "Users"
        ordering = ["created"]
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    # username = models.EmailField(max_length=254, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=254, unique=True, null=False, blank=False)
    nickname = models.CharField(max_length=254)
    birthday = models.CharField(max_length=254)
    # social = models.CharField(max_length=254)
    thumbail_image_url = models.CharField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # 헬퍼 클래스 사용
    objects = UserManager()
    
    # 사용자의 username field는 email으로 설정 (이메일로 로그인)
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return f'{self.id}({self.email})'

