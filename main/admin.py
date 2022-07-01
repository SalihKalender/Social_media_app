from django.contrib import admin
from .models import User, Post, Comment, Like, PPImage, Following, DissLike


class PostTree(admin.ModelAdmin):
    list_display = ('user_id', 'imageURL')
    search_fields = ('user_id',)

class CommentTree(admin.ModelAdmin):
    list_display = ('user_id', 'post_id', 'date')

class LikeTree(admin.ModelAdmin):
    list_display = ('user_id', 'post_id')

class PPImageTree(admin.ModelAdmin):
    list_display = ('user_id', 'imageURL')

class FollowingTree(admin.ModelAdmin):
    list_display = ('followed_user_id', 'following_user_id')

class DissLikeTree(admin.ModelAdmin):
    list_display = ('user_id', 'post_id')


admin.site.register(Post, PostTree)
admin.site.register(Comment, CommentTree)
admin.site.register(Like, LikeTree)
admin.site.register(PPImage, PPImageTree)
admin.site.register(Following, FollowingTree)
admin.site.register(DissLike, DissLikeTree)
