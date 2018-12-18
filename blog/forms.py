from django import forms
from .models import Post, Comment


class PostUpload(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('thumbnail', 'title', 'body')


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.IntegerField(widget=forms.Textarea)


class ReplyToComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ()
