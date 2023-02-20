"""
This file reads in data from files and stores it into a dictionary of dataclasses.
"""
import movie_dataclass
import rating_dataclass
from timeit import default_timer as timer

#reading movies from database
def read_movies(filename: str, large: bool):
    """
    :param filename: file that stores movie data from database
    :param large: whether the large datasets are being taken in or the small datasets
    :return: a dictionary of Movie objects
    """
    if large:
        print("reading data/title.basics.tsv into dict...")
    else:
        print("reading data/small.basics.tsv into dict...")
    start = timer()
    movie_dict = {}
    with open(filename, encoding='utf-8') as f:
        f.readline() #skips information line
        line = f.readline().rstrip("\n") #discards return line
        while line != "":
            datalist = line.split("\t")
            for i in datalist:
                if (i=="\\N"): #for when info is unapplicable
                    datalist[datalist.index(i)] = "0"
            if datalist[4] == "0": #Only add if not for adult
                datalist[8] = tuple(datalist[8].split(",")) #splitting genres into tuple
                movie_dict[datalist[0]] = movie_dataclass.Movies(*datalist)
            line = f.readline().rstrip("\n")
    elapsed = timer() - start
    print("elapsed time (s):", elapsed)
    print()
    return movie_dict

#reading ratings from database
def read_ratings(filename: str, movie_dict: dict, large: bool):
    """
    :param filename: file that stores ratings data from database
    :param large: whether the large data sets are being read or the small dataset
    :return: a dictionary of Rating objects
    """
    if large:
        print("reading data/title.ratings.tsv into dict...")
    else:
        print("reading data/small.ratings.tsv into dict...")
    start = timer()
    ratings_dict = {}
    with open(filename, encoding='utf-8') as f:
        f.readline() #skips information line
        line = f.readline().rstrip("\n") #discards return line
        while line != "":
            datalist = line.split("\t")
            try: #if the movie rating matches an existing movie add to list
                x = movie_dict[datalist[0]]
            except:
                pass
            else:
                ratings_dict[datalist[0]] = rating_dataclass.Ratings(*datalist)
            line = f.readline().rstrip("\n")
    elapsed = timer() - start
    print("elapsed time (s):", elapsed)
    print()
    return ratings_dict

