from domainmodel.movie import Movie
from datetime import datetime




class Review:
    def __init__(self,  movie:Movie, review_text : str, rating : int):
        self.__movie = movie
        self.__review_text = review_text
        self.__rating = None
        self.__timestamp = datetime.today()
        if type(rating) is int:
            if 0 < rating <= 10:
                self.__rating = rating



    @property
    def movie(self) -> Movie:
        return self.__movie

    @property
    def review_text(self) -> str:
        return self.__review_text
    @property
    def rating(self):
        return self.__rating
    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        return "<Review {}, {}>".format(self.movie, self.timestamp)

    def __eq__(self, other):
        if self.movie == other.movie and self.review_text == other.review_text \
            and self.rating == other.rating and self.timestamp == other.timestamp:
            return True
        return False

    def hash(self):
        return hash((self.movie, self.timestamp))