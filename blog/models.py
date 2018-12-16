from string import ascii_lowercase, digits

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from hashid_field import HashidAutoField
from PIL import Image
import sys
from io import BytesIO
from django.contrib.contenttypes.models import ContentType

IMG_SIZE = 2000, 2000
User = get_user_model()


class Post(models.Model):
    id = HashidAutoField(primary_key=True, alphabet=ascii_lowercase + digits)
    title = models.CharField(_('title'), max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('author'), related_name='authors')
    body = models.TextField(_('body'), blank=True)
    created_timestamp = models.DateTimeField(_('created timestamp'), auto_now_add=True)
    thumbnail = models.ImageField(default='mainBlog.png', upload_to='thumbnails/')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.thumbnail != 'mainBlog.png':
            im = Image.open(self.thumbnail)
            output = BytesIO()
            im.resize(IMG_SIZE)
            im.save(output, format='JPEG', quality=50)
            output.seek(0)
            self.thumbnail = InMemoryUploadedFile(output, 'ImageField', f"{self.thumbnail.name.split('.')[0]}.jpg",
                                                  'image/jpeg',
                                                  sys.getsizeof(output), None)

        super().save(force_insert, force_update, using, update_fields)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.id})

    def is_author(self, user: User):
        return user == self.author

    class Meta:
        ordering = ('-created_timestamp',)

    def __str__(self):
        return f'{self.title}'


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)

        return qs


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('post'), related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('author'), related_name='comments')
    body = models.TextField(_('body'))
    created_timestamp = models.DateTimeField(_('created timestamp'), auto_now_add=True)
    parent = models.ForeignKey('self', null=True, related_name='replies', on_delete=models.CASCADE, blank=True)
    # Todo: https://github.com/HonzaKral/django-threadedcomments/blob/master/threadedcomments/models.py Look into that.

    class Meta:
        ordering = ('-created_timestamp',)

    def __str__(self):
        return f'Comment #{self.id} by {self.author} for {self.post}'

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        return False if self.parent is not None else True
