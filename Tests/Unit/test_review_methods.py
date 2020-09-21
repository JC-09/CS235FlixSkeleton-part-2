from domainmodel.movie import Movie
from domainmodel.review import Review

class TestReviewMethods:
    def test_init(self):
        movie = Movie("Moana", 2016)
        review_text = "This movie was very enjoyable."
        rating = 8
        review = Review(movie, review_text, rating)

        assert repr(review.movie) == "<Movie Moana, 2016>"
        assert review.review_text == "This movie was very enjoyable."
        assert review.rating == 8