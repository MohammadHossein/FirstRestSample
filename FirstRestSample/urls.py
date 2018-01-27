"""FirstRestSample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from blog import views
from rest_framework.authtoken import views as restView

from blog.views import PostView, CommentView

# test()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.UserList.as_view()),
    path('login/', views.login_user),
    path('signup/', views.signup),
    path('delete/<str:username>/', views.user_detail),
    path('token/', views.token),
    path('gettoken/', restView.obtain_auth_token),
    url(r'^post/', PostView.as_view()),
    url(r'^comment/',CommentView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
