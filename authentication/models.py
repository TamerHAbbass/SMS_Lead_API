from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager)
from rest_framework_simplejwt.tokens import RefreshToken
import uuid

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        
        if email is None:
            raise TypeError('No email address detected')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):

    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }