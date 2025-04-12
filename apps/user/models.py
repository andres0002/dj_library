# django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# third
# own

# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, username, email, name, lastname, password, is_staff, is_superuser, **stra_fields):
        user = self.model(
            username = username,
            email = email,
            name = name,
            lastname = lastname,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **stra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, name, lastname, password=None, **stra_fields):
        return self._create_user(username, email, name, lastname, password, False, False, **stra_fields)

    def create_superuser(self, username, email, name, lastname, password=None, **stra_fields):
        return self._create_user(username, email, name, lastname, password, True, True, **stra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True, max_length=200)
    name = models.CharField(max_length=200, blank=True, null=True)
    lastname = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='user/profile/image/', max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'lastname']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']

    def __str__(self):
        return self.username