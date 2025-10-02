from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from .managers import CustomUserManager

# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):

    email = models.EmailField(_("email address"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="profile_images/",blank=True,null=True)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True,null=True)
    location = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=50, blank=True)
    timezone = models.CharField(max_length=50, blank=True)
    social_links = models.JSONField(blank=True, null=True)
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.email}"

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)