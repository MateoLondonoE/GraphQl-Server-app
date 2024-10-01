import graphene
import requests
from graphene_django import DjangoObjectType
from .models import Movie

# Reemplaza con tu API Key de OMDb
OMDB_API_KEY = '7f81358e'

# Definir el tipo de objeto Movie basado en el modelo Django
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie

# Tipo de objeto para las películas obtenidas desde OMDb
class OmdbMovieType(graphene.ObjectType):
    title = graphene.String()
    year = graphene.String()
    director = graphene.String()
    plot = graphene.String()
    imdb_rating = graphene.String()

# Query para buscar películas en OMDb y listar las locales
class Query(graphene.ObjectType):
    # Buscar película por título en OMDb
    movie_by_title = graphene.Field(OmdbMovieType, title=graphene.String(required=True))

    # Listar todas las películas guardadas en la base de datos local
    all_movies = graphene.List(MovieType)

    # Resolver para la consulta de OMDb
    def resolve_movie_by_title(self, info, title):
        url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return OmdbMovieType(
                title=data.get('Title'),
                year=data.get('Year'),
                director=data.get('Director'),
                plot=data.get('Plot'),
                imdb_rating=data.get('imdbRating')
            )
        else:
            raise Exception('Error fetching data from OMDb')

    # Resolver para listar películas locales
    def resolve_all_movies(self, info):
        return Movie.objects.all()


class CreateMovie(graphene.Mutation):
    movie = graphene.Field(MovieType)

    class Arguments:
        title = graphene.String(required=True)
        year = graphene.String(required=True)
        director = graphene.String(required=True)
        plot = graphene.String(required=True)
        imdb_rating = graphene.String(required=True)

    def mutate(self, info, title, year, director, plot, imdb_rating):
        movie = Movie(title=title, year=year, director=director, plot=plot, imdb_rating=imdb_rating)
        movie.save()
        return CreateMovie(movie=movie)

class UpdateMovie(graphene.Mutation):
    movie = graphene.Field(MovieType)

    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        year = graphene.String()
        director = graphene.String()
        plot = graphene.String()
        imdb_rating = graphene.String()

    def mutate(self, info, id, title=None, year=None, director=None, plot=None, imdb_rating=None):
        movie = Movie.objects.get(pk=id)

        if title:
            movie.title = title
        if year:
            movie.year = year
        if director:
            movie.director = director
        if plot:
            movie.plot = plot
        if imdb_rating:
            movie.imdb_rating = imdb_rating

        movie.save()
        return UpdateMovie(movie=movie)

class DeleteMovie(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        movie = Movie.objects.get(pk=id)
        movie.delete()
        return DeleteMovie(success=True)

# Agregar las mutaciones al esquema
class Mutation(graphene.ObjectType):
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()
    delete_movie = DeleteMovie.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
