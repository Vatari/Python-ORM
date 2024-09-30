import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
# Create and run your queries within functions
from main_app.models import Director, Movie, Actor
from django.db.models import Q, F, Count, Avg, Max


# 04 Django Queries Part One
def get_directors(search_name=None, search_nationality=None):

    if all([arg is None for arg in [search_name, search_nationality]]):
        return ""
    query = Q()

    if search_name and search_nationality is None:
        query = Q(full_name__icontains=search_name)
    elif search_name is None and search_nationality:
        query = Q(nationality__icontains=search_nationality)
    else:
        query = Q(full_name__icontains=search_name) & Q(nationality__icontains=search_nationality)

    directors = Director.objects.filter(query).order_by("full_name")
    result = []
    for director in directors:
        result.append(f"Director: {director.full_name}, nationality: {director.nationality}, experience: {director.years_of_experience}")

    if not result:
        return ""
    return "\n".join(result)


def get_top_director():

    director = Director.objects.get_directors_by_movies_count().first()
    if not director:
        return ""
    return f"Top Director: {director.full_name}, movies: {director.movie_count}."


def get_top_actor():

    actor = Actor.objects.annotate(movie_count=Count("movies"), average_rating=Avg("movies__rating")).order_by("-movie_count", "full_name").first()
    if not actor or not actor.movies.all():
        return ""
    movies_starring = []
    for movie in actor.movies.all():
        movies_starring.append(movie.title)

    return f"Top Actor: {actor.full_name}, starring in movies: {', '.join(movies_starring)}, movies average rating: {actor.average_rating:.1f}"


# 05 Django Queries Part Two
def get_actors_by_movies_count():

    actors = Actor.objects.annotate(movies_count=Count("actor_movies")).order_by("-movies_count", "full_name")[:3]

    result = []
    for actor in actors:
        if actor.movies_count:
            result.append(f"{actor.full_name}, participated in {actor.movies_count} movies")

    return "\n".join(result)


def get_top_rated_awarded_movie():

    movie = (Movie.objects
             .select_related("starring_actor")
             .prefetch_related("actors")
             .filter(is_awarded=True)
             .order_by("-rating", "title")
             .first())

    if not movie:
        return ""

    staring_actor = movie.starring_actor.full_name if movie.starring_actor else "N/A"

    cast = ", ".join(
        actor.full_name for actor in movie.actors.all().order_by("full_name")
    )

    return f"Top rated awarded movie: {movie.title}, rating: {movie.rating:.1f}. Starring actor: {staring_actor}. Cast: {cast}."


def increase_rating():

    query = Q(is_classic=True) & Q(rating__lt=10)
    classic_movies = Movie.objects.filter(query)

    if not classic_movies:
        return f"No ratings increased."

    count = classic_movies.aggregate(count_movies=Count("title"))["count_movies"]
    classic_movies.update(rating=F("rating") + 0.1)

    return f"Rating increased for {count} movies."


# actor = Actor()
# movie = Movie.objects.all().first()
# movie.actors.add(actor)

# print(Actor.objects.all())
# print(Movie.objects.all())
# # print(Movie.objects.all().first().actors.add(Actor.objects.all().first()))
# print(Movie.objects.all().first().actors.values("full_name").first()["full_name"])
# count = Actor.objects.aggregate(counted=Count("id"))["counted"]
# print(count)
# actors = Actor.objects.annotate(movies_count=Count("actor_movies")).order_by("-movies_count", "full_name")
# for actor in actors:
#     print(actor.movies_count)
#
# movies = Movie.objects.all()
# for movie in movies:
#     print(movie.starring_actor.full_name)
#
# for movie in movies:
#     for actor in movie.actors.all():
#         print(actor.full_name)
