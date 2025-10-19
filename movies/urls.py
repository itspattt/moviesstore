from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review,
        name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/',
        views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/',
        views.delete_review, name='movies.delete_review'),
    path('<int:id>/review/<int:review_id>/like/', views.like_review, name='movies.like_review'),
    path('petitions/', views.petition_list, name = "movies.petition_list"),
    path('petitions/new', views.create_petition, name = "movies.create_petition"),
    path('<int:id>/vote/', views.petition_vote, name = "movies.petition_vote"),
    path("map/", views.movie_map_page, name="movie_map_page"),                              # Renders the page
    path("map-data/", views.movie_map_data, name="movie_map_data"),                         # Processes map data
]