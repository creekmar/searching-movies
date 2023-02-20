"""
Dataclass for ratings
identifier: unique identifier for each movie
average: average ratings
votes: number of votes
"""

from dataclasses import dataclass
import operator

@dataclass()
class Ratings:
    identifier: str
    average: str
    votes: str

