from domainmodel.movie import Movie
from domainmodel.user import User
from domainmodel.review import Review
from activitysimulations.watchingsimulation import MovieWatchingSimulation
import pytest

@pytest.fixture
def simulator():
    return MovieWatchingSimulation(Movie("Star War", 2017))

def test_init(simulator):
    assert repr(simulator) == "Movie Watching Simulation - Star War : 2017\nNumber of users watching: 0\nNumber of reviews received: 0"

def test_adding_users_to_movie_watching_simulatior(simulator):
    user1 = User('user1_username', 'user1_password')
    user2 = User('user2_username', 'user2_password')

    simulator.add_user(user1)
    simulator.add_user(user2)

    assert simulator.number_of_users_watching == 2
    assert Movie("Star War", 2017) in user1.watched_movies
    assert Movie("Star War", 2017) in user2.watched_movies

def test_adding_reviews(simulator):
    user1 = User('user1_username', 'user1_password')
    user1_first_review = Review(Movie("Star War", 2017), "This is user1's first review for Star War", 9)
    user1_second_review = Review(Movie("Star War", 2017), "This is user1's second review for Star War", 9)
    user1_another_review = Review(Movie("Hunger Game", 2016), "This is user1's review for Hunger game", 8)
    user1.add_review(user1_first_review)
    user1.add_review(user1_second_review)
    user1.add_review(user1_another_review)

    user2 = User('user2_username', 'user2_password')
    user2_first_review = Review(Movie("Star War", 2017), "This is user2's first review for Star War", 6)
    user2.add_review(user2_first_review)

    simulator.add_user(user1)
    simulator.add_user(user2)
    simulator.retrieve_review()
    assert simulator.num_of_reviews == 3

def test_show_live_reviews(simulator):
    user1 = User('user1_username', 'user1_password')
    user1_first_review = Review(Movie("Star War", 2017), "This is user1's first review for Star War", 9)
    user1_second_review = Review(Movie("Star War", 2017), "This is user1's second review for Star War", 9)
    user1_another_review = Review(Movie("Hunger Game", 2016), "This is user1's review for Hunger game", 8)
    user1.add_review(user1_first_review)
    user1.add_review(user1_second_review)
    user1.add_review(user1_another_review)

    user2 = User('user2_username', 'user2_password')
    user2_first_review = Review(Movie("Star War", 2017), "This is user2's first review for Star War", 6)
    user2.add_review(user2_first_review)

    simulator.add_user(user1)
    simulator.add_user(user2)
    simulator.retrieve_review()
    assert simulator.show_live_reviews() == "Live Reviews for <Movie Star War, 2017>:\n<User user1_username>  --->  This is user1's first review " \
                                            "for Star War\n" + "<User user1_username>  --->  This is user1's second review for Star War\n" \
    + "<User user2_username>  --->  This is user2's first review for Star War\n"



def test_reper(simulator):
    user1 = User('user1_username', 'user1_password')
    user1_first_review = Review(Movie("Star War", 2017), "This is user1's first review for Star War", 9)
    user1_second_review = Review(Movie("Star War", 2017), "This is user1's second review for Star War", 9)
    user1_another_review = Review(Movie("Hunger Game", 2016), "This is user1's review for Hunger game", 8)
    user1.add_review(user1_first_review)
    user1.add_review(user1_second_review)
    user1.add_review(user1_another_review)

    user2 = User('user2_username', 'user2_password')
    user2_first_review = Review(Movie("Star War", 2017), "This is user2's first review for Star War", 6)
    user2.add_review(user2_first_review)

    simulator.add_user(user1)
    simulator.add_user(user2)
    simulator.retrieve_review()
    assert repr(simulator) == "Movie Watching Simulation - Star War : 2017\nNumber of users watching: 2\nNumber of reviews received: 3"

def test_equal(simulator):
    simulator_1 = MovieWatchingSimulation(Movie("Star War", 2017))
    simulator_2 = MovieWatchingSimulation(Movie("Star War", 1977))
    assert simulator.__eq__(simulator_1) == True
    assert simulator.__eq__(simulator_2) == False



