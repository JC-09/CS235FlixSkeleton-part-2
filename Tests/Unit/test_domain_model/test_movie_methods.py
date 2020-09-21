from domainmodel.model import Movie, Actor, Director, Genre
import pytest
class TestMovieMethods:
    def test_init(self):
        movie1 = Movie("Moana", 2016)
        assert repr(movie1) == "<Movie Moana, 2016>"

    def test_director(self):
        movie1 = Movie("Moana", 2016)
        movie1.director = Director("Ron Clements")
        assert repr(movie1.director) == "<Director Ron Clements>"

    def test_add_actors(self):
        movie1 = Movie("Moana", 2016)

        actors = [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]
        for actor in actors:
            movie1.add_actor(actor)
        assert movie1.actors == [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]

    def test_movie_runtime_minutes(self):
        movie1 = Movie("Moana", 2016)
        movie1.runtime_minutes = 107
        assert movie1.runtime_minutes == 107

        with pytest.raises(ValueError):
            movie1 = Movie("Kong", 2016)
            movie1.runtime_minutes = -6
            assert movie1.runtime_minutes == ValueError

    def test_remove_actor(self):
        movie1 = Movie("Moana", 2016)
        movie1.add_actor(Actor("Some Actor"))
        assert len(movie1.actors) == 1
        movie1.remove_actor(Actor("Some Actor"))
        assert len(movie1.actors) == 0
        movie1.remove_actor(Actor("Some Actor"))

    def test_hash_function(self):
        movie1 = Movie("Moana", 2016)
        assert movie1.__hash__() == hash(("Moana", 2016))

    def test_lt(self):
        movie1 = Movie("Moana", 2016)
        movie2 = Movie("Apple", 2019)
        movie3 = Movie("Apple", 2020)
        assert movie1.__lt__(movie2) == False
        assert movie2.__lt__(movie1) == True
        assert movie2.__lt__(movie3) == True
    def test_release_year(self):
        movie1 = Movie("Moana", 2016)
        movie2 = Movie("Apple", "abc")
        movie3 = Movie("Wrong", 1800)
        assert movie1.release_year == 2016
        assert movie2.release_year is None
        assert movie3.release_year is None