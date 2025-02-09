from django.db import models
from user.manager import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin




# Define the authentication providers
AUTH_PROVIDERS = {
    "email": "email",
    "google": "google",
    "linkedin": "linkedin",
    "github": "github",
}


class Role(models.Model):
    name = models.CharField(max_length=126, unique=True)

    class Meta:
        db_table = 'user_role'
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    def __str__(self):
        return self.name
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email"),unique=True)
    first_name = models.CharField(_("First Name"),max_length=255)
    last_name = models.CharField(_("Last Name"),max_length=255)
    otp = models.CharField(max_length=126, blank=True, null=True)
    roles = models.ManyToManyField(Role)
    is_active = models.BooleanField(_("Is this user active ?"), default=True)
    is_staff = models.BooleanField(_("Is this user staff ?"), default=False)
    is_registered = models.BooleanField(_("Is this user registered ?"), default=False)
    is_verified = models.BooleanField(_("Is this user verified ?"), default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    # Use choices for auth_provider
    AUTH_PROVIDERS_CHOICES = [(provider, provider) for provider in AUTH_PROVIDERS.values()]
    auth_provider = models.CharField(
        max_length=50,
        choices=AUTH_PROVIDERS_CHOICES,
        default=AUTH_PROVIDERS['email']
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'user_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email