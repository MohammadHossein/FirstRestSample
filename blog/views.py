from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import myUser
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.http import HttpResponse



class UserList(APIView):
    def get(self, request):
        users = myUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def token(request):
    username = request.data['username']
    password = request.data['password']
    print(username)
    print(password)
    print(myUser.objects.all()[0])
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
    print(myUser.objects.all()[0])
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        print('done')
        return HttpResponse('<p>hello</p>')
    return HttpResponse('<p>not login</p>')


@api_view(['POST'])
def signup(request):
    try:
        user = myUser()
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
        user = myUser.objects.get(username=username)
    except myUser.DoesNotExist:
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
