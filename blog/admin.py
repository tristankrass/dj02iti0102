from django.contrib import admin

from blog.models import Comment, Post


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ('body', 'parent')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ('post', 'author', 'body', 'parent',)
    list_display = ('body', 'created_timestamp', 'post', 'parent',)
    list_filter = ('post',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    fields = ('title', 'body', 'thumbnail',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        if formset.model == Comment:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.author = request.user
                instance.save()
        else:
            formset.save()
