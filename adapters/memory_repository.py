import csv
import os
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from adapters.repository import AbstractRepository
from domainmodel.model import User, Actor, Director, Genre, Movie, Review, WatchList, add_movie_attributes


class MemoryRepository(AbstractRepository):
    # Movies are ordered by title then by release year
    def __init__(self):
        self._users = list()
        self._actors = list()
        self._directors = list()
        self._genres = list()
        self._movies = list()
        self._reviews = list()
        self._watchlists = list()
        self._movie_index = dict()

    def add_user(self, user: User):
        if isinstance(user, User):
            self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.user_name == username.lower()), None)

    def get_user_watched_movies(self, user: User) -> List[Movie]:
        if user in self._users:
            return user.watched_movies
        return None

    def get_user_reviews(self, user: User) -> List[Review]:
        if user in self._users:
            return user.reviews
        return None

    def get_user_time_spent_watching_movies_minutes(self, user: User):
        if user in self._users:
            return user.time_spent_watching_movies_minutes
        return None

    def add_actor(self, actor: Actor):
        if isinstance(actor, Actor):
            self._actors.append(actor)

    def get_actor(self, actor_full_name) -> Actor:
        return next((actor for actor in self._actors if actor.actor_full_name == actor_full_name), None)

    def check_actor_existence_in_repo(self, actor: Actor) -> bool:
        if isinstance(actor, Actor):
            if actor in self._actors:
                return True
        return False

    def get_actor_colleague(self, actor: Actor) -> List[Actor]:
        if actor in self._actors:
            return actor.actor_colleague
        return None

    def get_total_number_of_actors(self) -> int:
        return len(self._actors)

    def add_director(self, director: Director):
        if isinstance(director, Director):
            self._directors.append(director)

    def get_director(self, director_full_name) -> Director:
        return next((director for director in self._directors if director.director_full_name == director_full_name),
                    None)

    def check_director_existence_in_repo(self, director: Director):
        if isinstance(director, Director):
            if director in self._directors:
                return True
        return False

    def get_total_number_of_directors(self) -> int:
        return len(self._directors)

    def add_genre(self, genre: Genre):
        if isinstance(genre, Genre):
            self._genres.append(genre)

    def get_genre(self, genre_name: str) -> Genre:
        return next((genre for genre in self._genres if genre.genre_name == genre_name), None)

    def get_total_number_of_genres_in_repo(self):
        return len(self._genres)

    def check_genre_existence(self, genre: Genre) -> bool:
        if isinstance(genre, Genre):
            if genre in self._genres:
                return True
        return False

    def add_movie(self, movie: Movie):
        if isinstance(movie, Movie):
            self._movies.append(movie)
            self._movie_index[movie.id] = movie

    def get_movie(self, title: str, release_year: int):
        return next((movie for movie in self._movies if (movie.title == title and movie.release_year == release_year)),
                    None)

    def get_total_number_of_movies_in_repo(self):
        return len(self._movies)

    def get_movie_by_index(self, index: int):
        movie = None

        try:
            movie = self._movie_index[index]
        except KeyError:
            pass
        return movie

    def get_movie_index_for_genre(self, genre_name: str):
        genre = next((genre for genre in self._genres if genre.genre_name == genre_name), None)
        if genre is not None:
            movie_indexes = [movie.id for movie in genre.classified_movies]
        else:
            movie_indexes = list()
        return movie_indexes

    def get_movie_actors(self, movie: Movie) -> List[Actor]:
        if movie in self._movies:
            return movie.actors
        return None

    def get_movie_release_year(self, movie: Movie) -> int:
        if movie in self._movies:
            return movie.release_year
        return None

    def get_movie_description(self, movie: Movie) -> str:
        if movie in self._movies:
            return movie.description
        return None

    def get_movie_director(self, movie: Movie) -> Director:
        if movie in self._movies:
            return movie.director
        return None

    def get_movie_reviews(self, movie: Movie):
        if movie in self._movies:
            return movie.reviews
        return None

    def get_movie_genres(self, movie: Movie) -> List[Genre]:
        if movie in self._movies:
            return movie.genres
        return None

    def get_movie_runtime_minutes(self, movie: Movie) -> int:
        if movie in self._movies:
            return movie.runtime_minutes
        return None

    def get_movies_by_index(self, index_list):
        # strip out any ids in the index_list that don't represent the Movie indexes in the repository
        existing_indexes = [index for index in index_list if index in self._movie_index]
        movies = [self._movie_index[index] for index in existing_indexes]
        return movies

    def add_review(self, review: Review):
        if isinstance(review, Review):
            super().add_review(review)
            self._reviews.append(review)

    def get_reviews(self) -> List[Review]:
        return self._reviews

    def get_total_number_of_reviews(self) -> int:
        return len(self._reviews)

    def add_watchlist(self, watchlist: WatchList):
        if isinstance(watchlist, WatchList):
            self._watchlists.append(watchlist)

    def get_watchlist(self) -> List[WatchList]:
        return self._watchlists


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_movies_actors_directors_genre_description(data_path: str, repo: MemoryRepository):
    genres = dict()
    for data_row in read_csv_file(os.path.join(data_path, "Data1000Movies.csv")):
        movie_index = int(data_row[0])
        title = data_row[1]

        list_of_genre_names = data_row[2].split(",")
        list_of_genres = [Genre(genre_name) for genre_name in list_of_genre_names]  # can have duplicate

        movie_description = data_row[3]

        director = Director(data_row[4])  # can have duplicate
        list_of_actor_names = data_row[5].split(",")
        list_of_actors = [Actor(actor_full_name) for actor_full_name in list_of_actor_names]  # can have duplicate

        release_year = int(data_row[6])
        runtime = int(data_row[7])

        # Create Movie object
        movie = Movie(
            title=title,
            release_year=release_year,
            id=movie_index
        )

        # Add movie to repo
        repo.add_movie(movie)

        # Add any new genres to repo
        # for genre in list_of_genres:
        #     if not repo.check_genre_existence(genre):
        #         repo.add_genre(genre)
        for genre in list_of_genres:
            if genre not in genres.keys():
                genres[genre] = list()
            genres[genre].append(movie_index)




        # Add any new actors to repo
        for actor in list_of_actors:
            if not repo.check_actor_existence_in_repo(actor):
                repo.add_actor(actor)

        # Add any new directors to repo
        if not repo.check_director_existence_in_repo(director):
            repo.add_director(director)


        # Connect the current movie with its attributes
        add_movie_attributes(movie=movie,
                             list_of_genres=list_of_genres,
                             description=movie_description,
                             list_of_actors=list_of_actors,
                             director=director,
                             runtime=runtime)

    # Associate Genres with Movies and add them to the repository
    for genre in genres.keys():
        for current_movie_index in genres[genre]:
            movie = repo.get_movie_by_index(current_movie_index)
            movie.add_genre(genre)
            genre.add_Movie(movie)
        repo.add_genre(genre)



def load_users(datapath: str, repo: MemoryRepository):
    users = dict()
    for data_row in read_csv_file(os.path.join(datapath, 'users.csv')):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[int(data_row[0])] = user
    return users


def load_reviews(data_path:str, repo:MemoryRepository, users):
    for data_row in read_csv_file(os.path.join(data_path, 'reviews.csv')):
        movie = repo.get_movie_by_index(int(data_row[2]))
        user = users[int(data_row[1])]
        review = Review(
            user=user,
            movie=movie,
            review_text=data_row[3],
            rating=int(data_row[4]),
            timestamp=datetime.fromisoformat(data_row[5])
        )
        user.add_review(review)
        movie.add_review(review)
        repo.add_review(review)


def populate(data_path:str, repo:MemoryRepository):
    # Load movies from Data1000Movies.csv
    load_movies_actors_directors_genre_description(data_path, repo)

    # Load users into the repository
    users = load_users(data_path, repo)

    # Load reviews into the repository
    load_reviews(data_path, repo, users)
