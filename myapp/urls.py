from django.urls import path
from .views import fetch_movie_data
from graphene_django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path('omdb/<str:movie_title>/', fetch_movie_data, name='fetch_movie_data'),
    path("graphql/", GraphQLView.as_view(graphiql=True, schema=schema)),
]
