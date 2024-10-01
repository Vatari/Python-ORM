from django.db.models import Manager, Count


class DirectorManager(Manager):

    def get_directors_by_movies_count(self):
        return self.annotate(movie_count=Count("movies")).order_by("-movie_count", "full_name")

