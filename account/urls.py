from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('user/profile/<int:user_id>/', views.show_profile, name='profile'),
    path('user/profile/edit/<int:pk>/', views.EditProfile.as_view(), name='edit_profile'),
]
