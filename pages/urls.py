from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_page, name='home_page'),
    path('game/detail/<slug:slug_path>/', views.show_detail, name='detail'),
    path('catalog/', views.CatalogPage.as_view(), name='catalog'),
    path('category/<int:cat_id>/', views.ShowGameRelatedCategories.as_view(), name='category'),

    path('like/<int:pk_product>/', views.like_logik, name='like_activa'),
    path('comment/<int:pk>/', views.add_reply, name='add_reply'),
    path('download/<slug:slug_path>/', views.download_file, name='download')
]
