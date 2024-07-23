from django.urls import path
from . import views

urlpatterns = [
    path('game-list/', views.GameList.as_view(), name='list-game'),
    path('game-detail/<slug:slug_path>/', views.GameDetail.as_view(), name='game-detail'),
    path('category-list/', views.CategoryList.as_view(), name='list-category'),
    path('category-detail/<int:cat_id>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('tag-list/', views.TagList.as_view(), name='list-tag'),
    path('tag-detail/<int:pk_path>/', views.TagDetail.as_view(), name='tag-detail'),
    path('favorite-list/', views.FavoriteList.as_view(), name='favorite-list')
]
