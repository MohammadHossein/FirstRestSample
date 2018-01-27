from django.test import TestCase

# Create your tests here.
from django.test import TestCase

# Create your tests here.
from blog.models import Post, MyUser, Comment


def test():
    # return
    adduser('test1','test1')
    adduser('test2','test2')
    post('this is test1 first post','test1')
    comment('this is test2 comment for psot','this is test1 first post','test2')
    comment('this is test1 comment for psot','this is test1 first post','test1')


def adduser(username,passsword):
    u = MyUser()
    u.username = username
    u.password = passsword
    u.save()
def post(text,username):
    p = Post()
    p.user = MyUser.objects.get(username=username)
    p.text = text
    p.save()

def comment(text,post,username):
    c = Comment()
    c.text = text
    c.post = Post.objects.get(text=post)
    c.user = MyUser.objects.get(username=username)
    c.save()