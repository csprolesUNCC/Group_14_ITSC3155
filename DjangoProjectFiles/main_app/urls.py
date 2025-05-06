from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('chats/', views.chats, name='chats'),
    path('create-listing/', views.createListing, name='create-listing'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('delete-profile-picture/', views.delete_profile_picture, name='delete_profile_picture'),
    path('item/<int:item_id>/', views.product, name='product'),
    path('delete-listing/<int:item_id>/', views.delete_listing, name='delete_listing'),
    path('edit-listing/<int:pk>/', views.edit_listing, name='edit_listing'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)