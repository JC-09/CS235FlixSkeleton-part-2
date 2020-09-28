from datetime import date

import pytest

from CS235Flix.adapters.repository import RepositoryException
from CS235Flix.domainmodel.model import User, Actor, Director, Genre, Movie, Review, WatchList


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', 123456789)
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_correct_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_total_number_of_movies_in_repo()
    assert number_of_movies == 10


def test_repository_can_retrieve_correct_director_count(in_memory_repo):
    number_of_directors = in_memory_repo.get_total_number_of_directors()
    assert number_of_directors == 10


def test_repository_can_retrieve_correct_actor_count(in_memory_repo):
    number_of_actors = in_memory_repo.get_total_number_of_actors()
    assert number_of_actors == 39


def test_repository_can_retrieve_correct_genre_count(in_memory_repo):
    number_of_genres = in_memory_repo.get_total_number_of_genres_in_repo()
    assert number_of_genres == 14


def test_repository_can_retrieve_correct_review_count(in_memory_repo):
    number_of_reviews = in_memory_repo.get_total_number_of_reviews()
    assert number_of_reviews == 3


def test_repository_can_retrieve_movies_by_year(in_memory_repo):
    movies_2014 = in_memory_repo.get_movies_by_release_year(2014)

    movies_2016 = in_memory_repo.get_movies_by_release_year(2016)
    assert len(movies_2014) == 1
    assert len(movies_2016) == 8


def test_repository_does_not_retrieve_any_movie_when_there_are_no_movies_for_a_given_year(in_memory_repo):
    movies_1800 = in_memory_repo.get_movies_by_release_year(1800)
    movies_2030 = in_memory_repo.get_movies_by_release_year(2030)
    assert len(movies_1800) == 0
    assert len(movies_2030) == 0


def test_repository_can_get_the_latest_movie(in_memory_repo):
    movie = in_memory_repo.get_latest_movie()
    assert movie.title == "The Lost City of Z"
    assert movie.release_year == 2016

def test_repository_can_get_the_oldest_movie(in_memory_repo):
    movie = in_memory_repo.get_oldest_movie()
    assert movie.title == "Prometheus"
    assert movie.release_year == 2012


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie(
        title="Avengers : End Game",
        release_year=2019,
        id=1050
    )
    in_memory_repo.add_movie(movie)

    assert in_memory_repo.get_movie_by_index(1050) is movie


def test_repository_can_retrieve_movie_by_index(in_memory_repo):
    movie = in_memory_repo.get_movie_by_index(1)

    # Check that the movie has expected attributes
    assert movie.title == "Guardians of the Galaxy"
    assert movie.release_year == 2014
    assert movie.description == "A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe."
    assert movie.director == Director("James Gunn")
    assert movie.runtime_minutes == 121
    actors = iter(movie.actors)
    assert next(actors) == Actor("Chris Pratt")
    assert next(actors) == Actor("Vin Diesel")
    assert next(actors) == Actor("Bradley Cooper")
    assert next(actors) == Actor("Zoe Saldana")

    # Check that the movie has the expected genre(s)
    assert movie.is_classified_as(Genre("Action"))
    assert movie.is_classified_as(Genre("Adventure"))
    assert movie.is_classified_as(Genre("Sci-Fi"))

    # Check that the movie has the correct reviews
    assert movie.number_of_reviews == 3

    review_1 = [review for review in movie.reviews if review.review_text == "This movie is great!"][0]
    review_2 = [review for review in movie.reviews if review.review_text == "This movie is awesome"][0]
    assert review_1.review_author.username == "fmercury"
    assert review_2.review_author.username == "thorke"


def test_repository_can_retrieve_movie_by_title_and_release_year(in_memory_repo):
    movie = in_memory_repo.get_movie("Guardians of the Galaxy", 2014)

    # Check that the movie has expected attributes
    assert movie.description == "A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe."
    assert movie.director == Director("James Gunn")
    assert movie.runtime_minutes == 121
    actors = iter(movie.actors)
    assert next(actors) == Actor("Chris Pratt")
    assert next(actors) == Actor("Vin Diesel")
    assert next(actors) == Actor("Bradley Cooper")
    assert next(actors) == Actor("Zoe Saldana")

    # Check that the movie has the expected genre(s)
    assert movie.is_classified_as(Genre("Action"))
    assert movie.is_classified_as(Genre("Adventure"))
    assert movie.is_classified_as(Genre("Sci-Fi"))

    # Check that the movie has the correct reviews
    assert movie.number_of_reviews == 3

    review_1 = [review for review in movie.reviews if review.review_text == "This movie is great!"][0]
    review_2 = [review for review in movie.reviews if review.review_text == "This movie is awesome"][0]
    assert review_1.review_author.username == "fmercury"
    assert review_2.review_author.username == "thorke"


def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie_by_index(99999)
    assert movie is None


def test_repository_can_retrieve_a_list_of_movie_indexes_by_a_genre_name(in_memory_repo):
    list_of_movie_indexes_for_Sci_Fi = in_memory_repo.get_movie_indexes_for_genre("Sci-Fi")
    list_of_movie_indexes_for_Horror = in_memory_repo.get_movie_indexes_for_genre("Horror")

    assert len(list_of_movie_indexes_for_Sci_Fi) == 2
    assert len(list_of_movie_indexes_for_Horror) == 1


def test_repository_returns_an_empty_list_of_movie_indexes_for_non_existent_genre_name(in_memory_repo):
    list_of_movie_indexes_for_Fake_Genre = in_memory_repo.get_movie_indexes_for_genre("Fake Genre")

    assert len(list_of_movie_indexes_for_Fake_Genre) == 0


def test_repository_can_retrieve_movies_for_a_indexes_list(in_memory_repo):
    movies = in_memory_repo.get_movies_by_index([1, 3, 7, 10])

    assert movies[0].title == 'Guardians of the Galaxy'
    assert movies[1].title == 'Split'
    assert movies[2].title == 'La La Land'
    assert movies[3].title == 'Passengers'


def test_repository_does_not_retrieve_movies_for_non_existent_indexes(in_memory_repo):
    movies = in_memory_repo.get_movies_by_index([2, 35455647])

    assert len(movies) == 1
    assert movies[0].title == "Prometheus"


def test_repository_returns_release_year_of_previous_movie(in_memory_repo):
    movie = in_memory_repo.get_movie_by_index(1)
    previous_year = in_memory_repo.get_release_year_of_previous_movie(movie)

    assert previous_year == 2012  # 2013 for 1000 movies


def test_repository_returns_none_when_there_are_no_previous_movies(in_memory_repo):
    movie = in_memory_repo.get_movie_by_index(2)
    previous_year = in_memory_repo.get_release_year_of_previous_movie(movie)

    assert previous_year is None


def test_repository_returns_release_year_of_next_movie(in_memory_repo):
    movie = in_memory_repo.get_movie_by_index(1)
    next_year = in_memory_repo.get_release_year_of_next_movie(movie)
    assert next_year == 2016 # 2015 if using the full 1000 movies


def test_repository_returns_none_when_there_are_no_next_movies(in_memory_repo):
    movie = in_memory_repo.get_movie_by_index(3)
    next_year = in_memory_repo.get_release_year_of_next_movie(movie)
    assert next_year is None


def test_repository_returns_an_empty_list_for_non_existent_indexes(in_memory_repo):
    movies = in_memory_repo.get_movies_by_index([22222, 33333])
    assert len(movies) == 0


def test_repository_can_add_an_actor(in_memory_repo):
    actor = Actor("Keanu Reeves")
    in_memory_repo.add_actor(actor)
    assert in_memory_repo.get_actor("Keanu Reeves") == actor


def test_repository_can_add_an_director(in_memory_repo):
    director = Director("Chad Stahelski")
    in_memory_repo.add_director(director)
    assert in_memory_repo.get_director("Chad Stahelski") == director


def test_repository_returns_none_for_non_existent_actor(in_memory_repo):
    assert in_memory_repo.get_actor("Fake Actor") is None


def test_repository_returns_none_for_non_existent_director(in_memory_repo):
    assert in_memory_repo.get_director("Fake Director") is None


def test_repository_can_check_existence_of_director(in_memory_repo):
    assert in_memory_repo.check_director_existence_in_repo(Director("Fake Director")) is False
    assert in_memory_repo.check_director_existence_in_repo(Director("Sean Foley")) is True


def test_repository_can_check_existence_of_actor(in_memory_repo):
    assert in_memory_repo.check_actor_existence_in_repo(Actor("Fake Actor")) is False
    assert in_memory_repo.check_actor_existence_in_repo(Actor("Matt Damon")) is True


def test_repository_can_check_existence_of_genre(in_memory_repo):
    assert in_memory_repo.check_genre_existence(Genre("Fake Genre")) is False
    assert in_memory_repo.check_genre_existence(Genre("Animation")) is True
    assert in_memory_repo.check_genre_existence(Genre("Family")) is True


def test_repository_can_get_reviews_from_a_movie(in_memory_repo):
    movie_reviews = iter(in_memory_repo.get_movie_reviews(in_memory_repo.get_movie_by_index(1)))

    assert next(movie_reviews).review_text == "This movie is great!"
    assert next(movie_reviews).review_text == "This movie is awesome"
    assert next(movie_reviews).review_text == "Love it!"
    with pytest.raises(StopIteration):
        assert repr(next(movie_reviews).review_text) == StopIteration


def test_repository_can_get_expected_movie_genres(in_memory_repo):
    movie_genres = iter(in_memory_repo.get_movie_genres(in_memory_repo.get_movie_by_index(10)))
    assert next(movie_genres) == Genre("Adventure")
    assert next(movie_genres) == Genre("Drama")
    assert next(movie_genres) == Genre("Romance")
    with pytest.raises(StopIteration):
        assert repr(next(movie_genres)) == StopIteration


def test_repository_can_add_a_watchlist(in_memory_repo):
    watchlist = WatchList()
    watchlist.add_movie(in_memory_repo.get_movie_by_index(3), date.today())
    watchlist.add_movie(in_memory_repo.get_movie_by_index(10), date.today())
    watchlist.add_movie(in_memory_repo.get_movie_by_index(16), date.today())
    watchlist.add_movie(in_memory_repo.get_movie_by_index(99), date.today())
    in_memory_repo.add_watchlist(watchlist)
    retrieved_watchlists = in_memory_repo.get_watchlist()

    assert len(retrieved_watchlists) == 1
    assert retrieved_watchlists[0].first_movie_in_watchlist() is in_memory_repo.get_movie_by_index(3)
    assert retrieved_watchlists[0].select_movie_to_watch(3) is in_memory_repo.get_movie_by_index(99)


def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie_by_index(3)
    review = Review(user=None, movie=movie, review_text="testing", rating=6, timestamp=date.today())
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_does_not_add_a_review_without_a_movie_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie_by_index(1)
    review = Review(user=user,
                    movie=None,
                    review_text="Awesome!",
                    rating=10,
                    timestamp=date.today())

    with pytest.raises(RepositoryException):
        # Exception expected because the Review doesn't refer to the Movie
        in_memory_repo.add_review(review)


