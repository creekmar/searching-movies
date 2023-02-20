"""
CSAPX Project 1: Movie Program
Takes in arguments from the command line to either go through the large data set or the small data set
Has 6 queries that go through the data and return movies that are related to the specific information that is put in

Author mec5765 Ming Creekmore
"""
import sys
import read_data
import queries

def main():
    #reading in datalists. Large by default and small if there is an argument
    if len(sys.argv)>1:
        movies_dict = read_data.read_movies(("data\\small.basics.tsv"))
        readings_dict = read_data.read_ratings("data\\small.ratings.tsv")
    else:
        movies_dict = read_data.read_movies("data\\title.basics.tsv", True)
        readings_dict = read_data.read_ratings("data\\title.ratings.tsv", movies_dict, False)

    #telling how many movies and ratings taken in
    print("Total movies:", len(movies_dict))
    print("Total ratings:", len(readings_dict))
    print()

    #reads each line to determine what to find
    for line in sys.stdin:
        new_line = line.rstrip("\n")
        par = new_line.split(" ")
        if par[0] == "LOOKUP":
            queries.lookup(readings_dict, par[1], movies_dict)
        elif par[0] == "CONTAINS":
            queries.contains(par[1], " ".join(par[2:]), movies_dict)
        elif par[0] == "YEAR_AND_GENRE":
            queries.year_and_genre(par[1], par[2], par[3], movies_dict)
        elif par[0] == "RUNTIME":
            queries.runtime(par[1], int(par[2]), int(par[3]), movies_dict)
        elif par[0] == "MOST_VOTES":
            queries.most_votes(par[1], int(par[2]), movies_dict, readings_dict)
        else:
            queries.top_num(par[1], int(par[2]), int(par[3]), int(par[4]), movies_dict, readings_dict)


if __name__ == '__main__':
    main()