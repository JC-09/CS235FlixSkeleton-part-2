from domainmodel.movie import Movie
from datetime import datetime
class WatchList:
    def __init__(self):
        self.__watchlist = list()
        self.__start_index = 0
        self.__schedule = dict();

    @property
    def watchlist(self):
        return self.__watchlist
    def add_movie(self, movie : Movie, date : datetime):
        if isinstance(movie, Movie):
            if movie not in self.__watchlist:
                self.__watchlist.append(movie)
                self.__schedule[movie] = date

    def remove_movie(self, movie : Movie):
        try:
            self.__watchlist.remove(movie)
            del self.__schedule[movie]
        except ValueError:
            return False

    def get_schedule(self):
        return self.__schedule

    def print_schedule(self):

        output_str = "You have scheduled the following movies to watch in the future: \n"
        sorted_schedule = sorted(self.__schedule.items(), key=lambda current:current[1], reverse=False)
        for movie in sorted_schedule:
            output_str += "Movie: " + str(movie[0].title) + ", " + str(movie[0].release_year) + " is schedule on " + str(movie[1].day) + "/" + \
                              str(movie[1].month) + "/" + str(movie[1].year) + "\n"
        return output_str

    def select_movie_to_watch(self, index:int):
        if index < 0:
            return None
        try:
            return self.__watchlist[index]
        except IndexError:
            return None

    def size(self):
        return len(self.__watchlist)

    def first_movie_in_watchlist(self):
        movie = None
        if self.size() > 0:
            movie = self.__watchlist[0]
        return movie

    def __iter__(self):
        return iter(self.__watchlist)

    def __next__(self):
        try:
            to_return = self.self.__watchlist[self.__start_index]
            self.__start_index += 1
            return to_return
        except IndexError:
            raise StopIteration

