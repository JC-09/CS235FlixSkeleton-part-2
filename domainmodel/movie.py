from domainmodel.genre import Genre
from domainmodel.actor import Actor
from domainmodel.director import Director

class Movie:
    def __init__(self, title : str, release_year : int):
        self.__description = ""
        self.__director = None
        self.__actors = list()
        self.__genres = list()
        self.__runtime_minutes = None

        if len(title) > 0 and type(title) is str and type(release_year) is int and release_year >= 1900:
            self.__title = title
            self.__release_year = release_year
        elif (title == "" or type(title) is not str ) and (type(release_year) is int and release_year >= 1900):
            self.__title = None
            self.__release_year = release_year
        elif (type(release_year) is not int) and (len(title) > 0 and type(title) is str ):
            self.__title = title
            self.__release_year = None
        else:
            self.__title = None
            self.__release_year = None
    @property
    def title(self) -> str:
        return self.__title

    @property
    def release_year(self) -> int:
        return self.__release_year

    @property
    def description(self) -> str:
        return self.__description

    @property
    def director(self) -> Director:
        return self.__director

    @property
    def actors(self) -> list():
        return self.__actors

    @property
    def genres(self) -> list():
        return self.__genres

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes



    @description.setter
    def description(self, new_description : str) -> bool:
        if type(new_description) is str:
            self.__description = new_description
            return True
        return False

    @director.setter
    def director(self, new_director) -> bool:
        if isinstance(new_director, Director):
            self.__director = new_director
            return True
        return False

    @runtime_minutes.setter
    def runtime_minutes(self, new_runtime_minutes) -> bool:
        if type(new_runtime_minutes) is int:
            if new_runtime_minutes > 0:
                self.__runtime_minutes = new_runtime_minutes
                return True
            else:
                raise ValueError
        return False



    def add_actor(self, actor : Actor) -> bool:
        if isinstance(actor, Actor):
            self.__actors.append(actor)
            return True
        return False

    def remove_actor(self, actor : Actor):
        if actor in self.__actors:
            self.__actors.remove(actor)


    def add_genre(self, genre : Genre) -> bool:
        if isinstance(genre, Genre):
            self.__genres.append(genre)
            return True
        return False

    def remove_genre(self, genre:Genre):
        if genre in self.__genres:
            self.__genres.remove(genre)


    def __repr__(self):
        return "<Movie {}, {}>".format(self.title, self.release_year)

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        return self.title == other.title and self.release_year == other.release_year
    def __lt__(self, other):
        if self.title == other.title:
            return self.release_year < other.release_year
        else:
            return self.title < other.title

    def __hash__(self):
        return hash((self.__title, self.__release_year))






















