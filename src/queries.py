"""
This file has all the query methods that can be performed on the dictionaries that house dataclasses
"""
#TODO update comments in function for param movie_dict

from timeit import default_timer as timer
import movie_dataclass
import operator

#look up a movie and rating by identifier
def lookup(rating_dict: dict, identifier: str, movie_dict: dict):
    """
    :param rating_dict: dictionary of ratings
    :param identifier: unique identifier for a movie
    :param movie_dict: dictionary of movies
    :return: nothing
    """
    start = timer()
    print("Processing: LOOKUP", identifier)
    try: #movie has to have a rating
        movie = movie_dict[identifier]
        rating = rating_dict[identifier]
    except:
        print("MOVIE NOT FOUND!\nRATING NOT FOUND!")
    else:
        print("MOVIE:", end=" ")
        output(movie, True)
        print("RATING:", "Identifier:", identifier, ", Rating: ", rating.average, ", Votes: ", rating.votes)
    elapsed = timer()-start
    print("elapsed time (s):", elapsed)
    print()


#find all movies of a certain type with specific words in the title
def contains(type: str, words: str, movie_dict: dict):
    """
    :param type: type of film as in short, tv, or movie
    :param words: words the title needs to contain
    :param movie_dict: dictionary of movies
    :return: nothing
    """
    start = timer()
    print("processing: CONTAINS ", type, words)
    found = False
    #outputting films that are a certain type and contains certain words
    for movie in movie_dict:
        temp = movie_dict[movie]
        if temp.primaryTitle.find(words)!=-1:
            if temp.type == type:
                output(temp, False)
                found = True
    if found == False: #if nothing is found
        print("\tNo match found!")
    elapsed = timer() - start
    print("elapsed time (s): ", elapsed)
    print()

#find all movies of a certain type and genre from a particular year
def year_and_genre(type: str, year: str, genre: str, movie_dict: dict):
    """
    :param type: type of film as in short, tv, or movie
    :param year: year the movie is from
    :param genre: genre the movie is under
    :param movie_dict: dictionary of movies
    :return: nothing
    """
    start = timer()
    movie_list = []
    print("processing: YEAR_AND_GENRE", type, year, genre)
    #add to list if film is a certain type, year, and genre
    for movie in movie_dict:
        temp = movie_dict[movie]
        if temp.startYear == year:
            if genre in temp.genre:
                if temp.type == type:
                    movie_list.append(temp)

    #determining output
    if len(movie_list) > 0:
        #sorting list alphabetically then printing out
        movie_list.sort(key=operator.attrgetter('primaryTitle'))
        for movie in movie_list:
            output(movie, False)
    else:
        #if no match found
        print("\tNo match found!")
    elapsed = timer() - start
    print("elapsed time (s): ", elapsed)
    print()

#find movies of certain type that are within a range of runtimes
def runtime(type: str, min_minutes: int, max_minutes: int, movie_dict: dict):
    """
    :param type: Type of film as in short, tv, or movie
    :param min_minutes: the minimum runtime in minutes
    :param max_minutes: the maximum runtime in minutes
    :param movie_dict: dictionary of movies
    :return: nothing
    """
    start = timer()
    print("processing: RUNTIME", type, min_minutes, max_minutes)
    movie_list = []
    #adding movie to list if it is in a certain type and within the time
    for movie in movie_dict:
        temp = movie_dict[movie]
        time = int(temp.runtime)
        if min_minutes == max_minutes:
            if time == min_minutes:
                if temp.type == type:
                    movie_list.append(temp)
        elif time >= min_minutes and time <= max_minutes:
            if temp.type == type:
                movie_list.append(temp)

    #determining output
    if len(movie_list) > 0:
        #sorting list alphabetically and by runtimes
        movie_list.sort(key=operator.attrgetter('primaryTitle'))
        movie_list.sort(key=operator.attrgetter('runtime'), reverse=True)
        for movie in movie_list:
            output(movie, False)
    else:
        #if no match found
        print("\tNo match found!")
    elapsed = timer() - start
    print("elapsed time (s): ", elapsed)
    print()

#find a given number of movies of a certain type with the most votes
def most_votes(type: str, num: int, movie_dict: dict, rating_dict: dict):
    """
    :param type: type of film as in short, movie, tv
    :param num: number of movies to find
    :param movie_dict: dictionary of movies
    :param rating_dict: dictionary of ratings
    :return: nothing
    """
    start = timer()
    print("processing: MOST_VOTES", type, num)
    new_dict = {}
    for rating in rating_dict:
        #if it is the right type add to new rating dictionary
        temp = movie_dict[rating]
        if temp.type == type:
            new_dict[rating] = [temp.primaryTitle, int(rating_dict[rating].votes)]

    # determining output
    if len(new_dict) > 0:
        # sorting list alphabetically and by number of votes then output
        new_dict = top(new_dict, num, 1)
        new_dict = dict(sorted(new_dict.items(), key = lambda i: i[1][0]))
        new_dict = dict(sorted(new_dict.items(), key = lambda i: i[1][1], reverse=True))
        count = 1
        for rating in new_dict:
            print("\t", count, ". VOTES: ", new_dict[rating][1], " MOVIE: ", sep="", end="")
            output(movie_dict[rating], True)
            count+=1
    else:
        # if no match found
        print("\tNo match found!")
    elapsed = timer() - start
    print("elapsed time (s): ", elapsed)
    print()

#Find a certain number of movies of certain type within a range of years
#that are the highest rated and have at least 1000 votes
def top_num(type: str, num: int, startyear: int, endyear: int, movie_dict: dict, rating_dict: dict):
    """
    :param type: type of film as in movie, tv, or short
    :param num: number of movies to find
    :param startyear: year to start searching
    :param endyear: year to end searching
    :param movie_dict: dictionary of movies
    :param rating_dict: dictionary of ratings
    :return: nothing
    """
    start = timer()
    print("processing: TOP", type, num, startyear, endyear)
    for i in range(startyear, endyear+1):
        print("\tYEAR:", i)
        new_dict = {}
        for rating in rating_dict:
            temp = movie_dict[rating]
            if int(temp.startYear) == i:
                if int(rating_dict[rating].votes) >= 1000:
                    if temp.type == type:
                        new_dict[rating] = [temp.primaryTitle, int(rating_dict[rating].votes), float(rating_dict[rating].average)]
        #determinging output for each list for each year
        if len(new_dict)>0:
            #sorting alphabetically, then by votes, then by rating
            new_dict = top(new_dict, num, 2)
            new_dict = dict(sorted(new_dict.items(), key=lambda i: i[1][0]))
            new_dict = dict(sorted(new_dict.items(), key=lambda i: i[1][1], reverse=True))
            new_dict = dict(sorted(new_dict.items(), key=lambda i: i[1][2], reverse=True))
            count = 1
            for rating in new_dict:
                print("\t\t", count, ". RATING: ", new_dict[rating][2], " VOTES: ", new_dict[rating][1], " MOVIE: ", sep="", end="")
                output(movie_dict[rating], True)
                count += 1
        else:
            #if no match found
            print("\tNo match found!")
    elapsed = timer() - start
    print("elapsed time (s): ", elapsed)
    print()

def output(movie: movie_dataclass.Movies, top: bool):
    """
    :param movie: a movie object to be printed
    :param top: whether there are ratings outputted before or not
    :return: nothing
    """
    if not top:
        #if there are no ratings printed before then tab
        print("\t", end="")
    print("Identifier:", movie.identifier, ", Title:", movie.primaryTitle, ", Type:", movie.type, ", Year:",
            movie.startYear, end=" , ")
    print("Runtime:", movie.runtime, ", Genres:", ','.join([str(i) for i in movie.genre]))

def top(rating_dict: dict, num: int, item: int):
    """
    :param rating_dict: dictionary of ratings with values of identifiers
    :param num: number of movies to find
    :param item: the index of the list to use for sorting
    :return: a ditionary of the top movies
    """
    top_dict = {}
    if len(rating_dict)<num:
        num = len(rating_dict)
    #find a certain number of top votes and add them to a list
    for i in range(num):
        top = max(rating_dict.items(), key = lambda i: i[1][item])
        top_dict[top[0]] = top[1]
        rating_dict.pop(top[0])
    return top_dict
