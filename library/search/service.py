from library.adapters.repository import AbstractRepository
#import library.adapters.repository as repo
from library.domain.model import Book, Review
from typing import Union



def find_books_by_year(year:int, repo: AbstractRepository) -> Union[list,None]:
    try :
        year = int(year)
    except ValueError:
        return []
    returnedBooks = repo.search_by_year(year)
    if returnedBooks == []:
        return  []
    return returnedBooks

def find_books_by_author(author:str, repo: AbstractRepository) -> Union[list,None]:
    returnedBooks = repo.search_by_author(author)
    if returnedBooks == []:
        return []
    return returnedBooks

def find_books_by_publisher(publisher:str, repo: AbstractRepository) -> Union[list,None]:
    returnedBooks = repo.search_by_publisher(publisher)
    if returnedBooks == []:
        return []
    return returnedBooks