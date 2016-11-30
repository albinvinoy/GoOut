import tmdbsimple as tmdb
from django.conf import settings
from enum import Enum

class Genre(Enum):
    animation = 16
    horror = 27
    action = 28
    romance = 10749
    other = -1

class MovieInfo:
    tmdb.API_KEY = settings.MOVIE_API_KEY

    def __init__(self):
        self.movies = tmdb.Movies()
        self.now_playing = self.movies.now_playing()

    def GetGenreFromGenreName(self, genreName):
        if (genreName == 'Action'):
            return Genre.action
        elif (genreName == 'Horror'):
            return Genre.horror
        elif (genreName == 'Animation'):
            return Genre.animation
        elif (genreName == 'Romance'):
            return Genre.romance
        else:
            return Genre.other

    def GetPopularMoviesInGenre(self, genre):
        tmdb_genre = tmdb.Genres(genre.value)
        movies_in_genre = tmdb_genre.movies(page=10)
        return movies_in_genre['results']

    def GetNowPlayingInGenre(self, genre):
        movies_in_genre = [movie for movie in self.now_playing['results'] if genre.value in movie['genre_ids']]
        return movies_in_genre