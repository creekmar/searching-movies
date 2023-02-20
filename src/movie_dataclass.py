"""
dataclass for movies

identifier: unique identifier
type: type of film as in movie, short, tv
primaryTitle: most known title right now
originalTitle: first title
isAdult: is it restricted by age
startYear: year it came out/started
endYear: year it ended (for tv or shorts)
runtime: how long the film runs
genre: genre of film
"""

from dataclasses import dataclass
import operator

@dataclass
class Movies:
    identifier: str
    type: str
    primaryTitle: str
    originalTitle: str
    isAdult: str
    startYear: str
    endYear: str
    runtime: str
    genre: str

