from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.core.validators import URLValidator
from django.utils.translation import ugettext_lazy as _
from allauth.socialaccount.models import SocialAccount


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

    # def save(self, *args, **kwargs):
    #     self.avatar_url = SocialAccount.objects.filter(username=self.get_username()).extra_data.get('avatar_url')
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.username}'
