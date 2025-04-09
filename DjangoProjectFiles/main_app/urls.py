from django.urls import path
from . import views

urlpatterns = [
    # defined a randon view for home so I could view the page
    path('', views.chats, name='home'),
    path('chats/', views.chats, name='chats'),
]