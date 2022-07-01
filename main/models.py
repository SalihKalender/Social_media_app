from email.policy import default
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User



class Post(models.Model):
    imageURL = models.ImageField(upload_to='post_images')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    content = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)

class DissLike(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)


class PPImage(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    imageURL = models.ImageField(upload_to='profile_images')

class Following(models.Model):
    followed_user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name = 'followed')
    following_user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name = 'following')