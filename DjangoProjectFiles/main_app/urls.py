from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('chats/', views.chats, name='chats'),
    path('create-listing/', views.createListing, name='create-listing'),
]
