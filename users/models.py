from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.core.validators import URLValidator
from django.utils.translation import ugettext_lazy as _
from allauth.socialaccount.models import SocialAccount
from allauth.account.signals import user_signed_up


class User(AbstractUser):
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    avatar_url = models.TextField(
        _('Avatar of the github user'), blank=True, validators=[URLValidator])
    avatar = models.ImageField(default='default.png', upload_to='avatars/')
    follows = models.ManyToManyField('User', related_name='followed_by')

    @property
    def get_full_name(self):
        return super().get_full_name()

    def get_short_name(self):
        return super().get_short_name()

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def __str__(self):
        return f'{self.username}'


@receiver(user_signed_up)
def social_login_profilepic(sociallogin, user, **kwargs):
    picture_url = ''
    if sociallogin:
        if sociallogin.account.provider == 'github':
            picture_url = sociallogin.account.get_avatar_url()
    user.avatar_url = picture_url
    user.save()
