# coding=utf-8
from django.contrib import admin
from stream.models import *

# Inline
class PostInline(admin.StackedInline):
    model = Post

class CommentInline(admin.StackedInline):
    model = Comment

# ModelsAdmin
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'post_content')
    inlines = [CommentInline,]
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'post_id', 'comment_content')

# Register
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
