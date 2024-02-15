from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('login', views.views_login, name='login'),
    path('signup', views.views_signup, name = 'signup'),
    path('logout', views.views_logout, name = 'logout'),
    path('', views.home, name = 'home'),
    path('upload', views.views_upload_image, name = 'upload'),
]
