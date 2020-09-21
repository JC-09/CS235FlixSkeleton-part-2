from domainmodel.user import User
from domainmodel.movie import Movie
from domainmodel.review import Review

class TestUserMethods:
    def test_init(self):
        user1 = User('Martin', 'pw12345')
        user2 = User('Ian', 'pw67890')
        user3 = User('Daniel', 'pw87465')
        assert repr(user1) == "<User martin>"
        assert repr(user2) == "<User ian>"
        assert repr(user3) == "<User daniel>"

    def test_watched_movies(self):
        user1 = User('user1', 'pw12345')
        movie1 = Movie("Star War", 19879)
        movie1.runtime_minutes = 120
        user1.watch_movie(movie1)
        assert user1.watched_movies == [movie1]
        assert user1.time_spent_watching_movies_minutes == 120

    def test_add_review(self):
        user1 = User('user1', 'pw12345')
        movie1 = Movie("Star War", 19879)
        movie1.runtime_minutes = 120
        user1.watch_movie(movie1)
        review = Review(movie1, "This is a great movie!", 9)
        user1.add_review(review)

        assert user1.reviews == [review]