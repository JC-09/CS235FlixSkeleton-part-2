from CS235Flix.adapters.datafilereaders import MovieFileCSVReader


def main():
    filename = 'CS235Flix/adapters/datafiles/Data1000Movies.csv'
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()



if __name__ == "__main__":
    main()