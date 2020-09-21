from domainmodel.movie import Movie
from domainmodel.review import Review

class User:
    def __init__(self, user_name : str, password : str):
        self.__user_name = None
        self.__password = None
        if type(user_name) is str:
            if len(user_name) > 0:
                self.__user_name = user_name.lower()
        if type(password) is str:
            if len(password) > 0:
                self.__password = password
        self.__watched_movies = list()
        self.__reviews  = list()
        self.__time_spent_watching_movies_minutes = 0

    @property
    def user_name(self):
        return self.__user_name

    @property
    def password(self):
        return self.__password

    @property
    def watched_movies(self):
        return self.__watched_movies

    @property
    def reviews(self):
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent_watching_movies_minutes

    def __repr__(self):
        return "<User {}>".format(self.user_name)

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        if self.user_name is None and other.user_name is None:
            return False
        return self.user_name == other.user_name

    def __lt__(self, other):
        return self.user_name < other.user_name

    def __hash__(self):
        return hash((self.__user_name, self.__password))

    def watch_movie(self, movie : Movie):
        if isinstance(movie, Movie):
            if movie not in self.__watched_movies:
                self.__watched_movies.append(movie)
                self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review : Review):
        if isinstance(review, Review):
            if review not in self.__reviews:
                self.__reviews.append(review)
