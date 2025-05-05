from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('chats/', views.chats, name='chats'),
    path('create-listing/', views.createListing, name='create-listing'),
    path('profile/', views.profile, name='profile'),
    path('item/<int:item_id>/', views.product, name='product'),
    path('delete-listing/<int:item_id>/', views.delete_listing, name='delete_listing'),
    path('edit-listing/<int:pk>/', views.edit_listing, name='edit_listing'),
    path('search/', views.search_page, name='search'),
]
