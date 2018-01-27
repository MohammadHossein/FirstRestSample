from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from blog.models import Post, Comment
from blog.serializers import PostSerializer, CommentSerializer
from .models import MyUser
from .serializers import UserSerializer
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.http import HttpResponse


class UserList(APIView):
    def get(self, request):
        users = MyUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class PostView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        if str(request.user) != request.data['username']:
            return Response('Can\'t post with other users!', status=status.HTTP_403_FORBIDDEN)
        p = Post()
        p.text = request.data['text']
        p.user = MyUser.objects.get(username=request.data['username'])
        p.save()
        return Response('New post added!', status=status.HTTP_200_OK)

    def put(self, requset):
        p = Post.objects.get(postId=requset.data['id'])
        p.text = requset.data['text']
        p.save()
        return Response('Post changed!', status=status.HTTP_200_OK)

    def delete(self, requset):
        p = Post.objects.get(postId=requset.data['id'])
        p.delete()
        return Response('Post deleted!', status.HTTP_200_OK)


class CommentView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, requset):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        c = Comment()
        c.text = request.data['text']
        c.user = MyUser.objects.get(username=request.data['username'])
        c.post = Post.objects.get(postId=request.data['id'])
        c.save()
        return Response('New comment added!', status=status.HTTP_200_OK)

    def put(self, requset):
        c = Comment.objects.get(commentId=requset.data['id'])
        c.text = requset.data['text']
        c.save()
        return Response('Comment Changed!', status=status.HTTP_200_OK)

    def delete(self, requset):
        c = Comment.objects.get(commentId=requset.data['id'])
        c.delete()
        return Response('Comment deleted!', status.HTTP_200_OK)


@api_view(['POST'])
def token(request):
    username = request.data['username']
    password = request.data['password']
    print(username)
    print(password)
    print(MyUser.objects.all()[0])
    user = authenticate(username=username, password=password)
    if user:
        # login(request, user)
        print('done')
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return HttpResponse('<p>not login</p>')


@api_view(['POST'])
def login_user(request):
    username = request.data['username']
    password = request.data['password']
    print(username)
    print(password)
    print(MyUser.objects.all()[0])
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        print('done')
        return HttpResponse('<p>hello</p>')
    return HttpResponse('<p>not login</p>')


@api_view(['POST'])
def signup(request):
    try:
        user = MyUser()
        user.username = request.data['username']
        user.set_password(request.data['password'])
        print(user.username)
        print(user.password)
        user.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def user_detail(request, username):
    try:
        user = MyUser.objects.get(username=username)
    except MyUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        print("delete done")
        return Response(status=status.HTTP_204_NO_CONTENT)
