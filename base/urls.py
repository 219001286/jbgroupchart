from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.Home, name="home"),
    path('departments/<str:pk>/', views.Room, name="room"),
    path('profile/<str:pk>/',views.userProfile, name="user_profile"),
    path('create_department/', views.createDepartment, name="create_department"),
    path('update_department/<str:pk>/', views.UpdateDepartment, name="update_department"),
    path('delete_department/<str:pk>/', views.deleteDepartment, name="delete_department"),
    path('delete_message/<str:pk>/', views.deleteMessage, name="delete_message"),
    path('Update_user/', views.UpdateUser, name="update-user"),
    path('Topics/', views.TopicPage, name="topic"),
    path('Activity/', views.Activity, name="activity"),
]
  