from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('user-view/', views.user_view, name='user_view'),
    path('user-view/create', views.user_view_create, name='user_view_create'),
]