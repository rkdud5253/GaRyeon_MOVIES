from django.urls import path
from . import views


app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/comments/', views.movie_create_comment, name='movie_create_comment'),
    path('<int:movie_pk>/comments/<int:comment_pk>/delete/', views.movie_comments_delete, name='movie_comments_delete'),
    path('recommend/', views.recommend, name='recommend'),
    path('recommendpopularity/', views.recommendpopularity, name='recommendpopularity'),
    path('recommendvoteaverage/', views.recommendvoteaverage, name='recommendvoteaverage'),
    path('recommendgenre/', views.recommendgenre, name='recommendgenre'),
]