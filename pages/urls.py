from django.urls import path
from . import views


urlpatterns = [
    # path('url путь к странице', функция отвечающая за логику, name='имя путь')
    path('', views.index_page, name='home_page'),
    path('category/<int:cat_id>/', views.show_game_by_cat_id, name='category'),
    path('game/detail/<slug:slug_path>/', views.show_detail, name='detail'),
    # =========================
    path('account/login/', views.login_view, name='login'),
    path('account/register/', views.register_view, name='register'),
    path('account/logout/', views.login_view, name='logout'),
    # =========================
    path('like/<int:pk_product>/', views.like_logik, name='like_activa'),
    path('comment/<int:pk>/', views.add_reply, name='add_reply'),
    path('download/<slug:slug_path>/', views.download_file, name='download')
]
