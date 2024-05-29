from django.urls import path
from . import views


urlpatterns = [
    path('account/login/', views.login_view, name='login'),
    path('account/register/', views.register_view, name='register'),
    path('account/logout/', views.login_view, name='logout')
]
