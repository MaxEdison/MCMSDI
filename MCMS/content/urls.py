from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('images/', views.image_list, name='image_list'),
    path('articles/', views.article_list, name='article_list'),
    path('photographers/', views.photographer_list, name='photographer_list'),
    path('writers/', views.writer_list, name='writer_list'),
    path('photographer/<str:photographer_code>/', views.photographer_images, name='photographer_images'),
    path('writer/<str:writer_code>/', views.writer_articles, name='writer_articles'),
    path('update_data/<int:image_id>/', views.api_req, name='update_data'),
]
