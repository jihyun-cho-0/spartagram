# tweet/models.py
from django.db import models
from user.models import UserModel
from taggit.managers import TaggableManager
from django.conf import settings
from user.models import UserModel

# Create your models here.
class TweetModel(models.Model):
    class Meta:
        db_table = "tweet"

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=256)
    imgfile = models.ImageField(null=True, upload_to="tweet/", blank=True)
    # 내가 좋아요 누른 게시글 = like_content, 다른 사람이 좋아요 누른 게시글 = like_user
    like_content = models.ManyToManyField(UserModel, related_name='like_user')
    save_content = models.ManyToManyField(UserModel, related_name='save_user', blank=True)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TweetComment(models.Model):
    class Meta:
        db_table = "comment"
    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)