from app.models import UserInfo, UserInterest
from app.apis.movies import MovieInfo
from collections import Counter
import random

class Newsfeed:
    def __init__(self, user, pageSize=10):
        self.userInfo = user
        self.userInterests = UserInterest.objects.filter(user=self.userInfo)
        self.userSubinterests = set()
        for userInterest in self.userInterests:
            self.userSubinterests.update(userInterest.subinterests.all())
        self.pageSize=pageSize
        self.articles = []

    def nextPage(self):
        articleSubinterests = [random.choice(list(self.userSubinterests)) for _ in range(self.pageSize)]
        subinterestCounts = Counter(articleSubinterests)
        for key, value in subinterestCounts.most_common():
            subinterest = key
            subinterestCount = value
            interest = subinterest.interest
            if (interest.id == 1):
                # Call movie API
                movies = MovieInfo()
                genre = movies.GetGenreFromGenreName(subinterest.name)
                genre_movies = movies.GetPopularMoviesInGenre(genre)
                if (len(genre_movies) < subinterestCount):
                    subinterestCount = len(genre_movies)
                selected_movies = random.sample(genre_movies, subinterestCount)
                self.articles.extend(list(map((lambda movie: {
                    'interest':interest.name,
                    'subinterest':subinterest.name,
                    'title':movie['title'],
                    'overview':movie['overview'],
                    'release_date':movie['release_date'],
                }), selected_movies)))
            elif (interest.id == 2):
                # Call music API
                self.articles.extend([])
            elif (interest.id == 3):
                # Call beer API
                self.articles.extend([])
            elif (interest.id == 4):
                # Call car API
                self.articles.extend([])
        return self.articles
