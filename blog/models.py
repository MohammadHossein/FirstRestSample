from django.contrib.auth.models import User
from django.db import models


class MyUser(User):
    pass

    def __str__(self):
        return '%s : %s' % (self.username, self.password)


class Post(models.Model):
    user = models.ForeignKey(MyUser, related_name='post_user', on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    date = models.DateTimeField(auto_now=True)
    postId = models.AutoField(primary_key=True)

    def __str__(self):
        return '%s : %s' % (self.user, self.text)


class Comment(models.Model):
    user = models.ForeignKey(MyUser, related_name='comment_user', on_delete=models.CASCADE)
    text = models.CharField(max_length=140)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    commentId = models.AutoField(primary_key=True)

    def __str__(self):
        return '%s : %s' % (self.user.username, self.text)

    class Meta:
        unique_together = ('post', 'commentId',)
        ordering = ('commentId',)
