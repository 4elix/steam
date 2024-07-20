from django.urls import path
from . import views

urlpatterns = [
    path('game-list/', views.game_list, name='list-game'),
    path('game-detail/<slug:slug_path>/', views.game_detail, name='game-detail'),
    path('category-list/', views.category_list, name='list-category'),
    path('category-detail/<int:cat_id>/', views.category_detail, name='category-detail'),
    path('tag-list/', views.tags_game_list, name='list-tag'),
    path('tag-detail/<int:pk_path>/', views.tags_detail, name='tag-detail')
]
