from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
import random


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, password, **extra_fields):
        """
            Create and save a User with the given email and password.
            """
        if not phone_number:
            raise ValueError('The Email must be set')
        if not password:
            raise ValueError('The Password must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        """
            Create and save a SuperUser with the given email and password.
            """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    username = None
    date_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=40, unique=True, verbose_name=_('phone_number'), null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, verbose_name=_('created_at'))
    mycode = models.IntegerField(null=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    def __str__(self):
        return f"{self.phone_number}"

    @classmethod
    def mycode2(self):
        return random.randint(100000, 999999)

    def save(self, *args, **kwargs):
        self.mycode = self.mycode2()
        super().save(*args, **kwargs)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'id': str(self.id),
            'code': self.mycode
        }


class Map(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='map', verbose_name=_('user'))
    title = models.CharField(max_length=120, verbose_name=_('title'), null=True, blank=True)
    phone_number = models.IntegerField(verbose_name=_('phone_number'), null=True, blank=True)
    address = models.CharField(max_length=300, verbose_name=_('address'))
    region = models.CharField(max_length=300, verbose_name=_('region'), null=True, blank=True)
    town = models.CharField(max_length=200, verbose_name=_('town'))
    created_at = models.DateField(auto_now_add=True, verbose_name=_('created_at'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('update_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Map')
        verbose_name_plural = _('Maps')
