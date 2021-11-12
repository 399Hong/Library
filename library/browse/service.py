
from library.adapters.repository import AbstractRepository
#import library.adapters.repository as repo
from library.domain.model import Book, Review
from typing import Union

class NonExistentBulkException(Exception):
    pass
class NonExistentBookException(Exception):
    pass

class UnknownUserException(Exception):
    pass

# test cases
def get_book_bulk(currentPos:int,size:int,repo: AbstractRepository) -> list:
    info =  repo.get_book_by_bulk(currentPos,size)
    if info == None:
        raise NonExistentBulkException
    else: 
        return info
   

def get_book_by_id(id:int,repo: AbstractRepository) -> Book:
    book = repo.get_book(id) 
    if book == None:
        raise NonExistentBookException
    else:
        return book


def get_reviews_for_book(id, repo: AbstractRepository) ->  Union[list,None]:
    return repo.get_reviews_by_id(id)



def add_review(user_name: str, id: int, review_text: str, rating:int, repo: AbstractRepository):
    # Check that the book exists and get book
    book = repo.get_book(id)
    if book is None:
        raise NonExistentBookException
    # Check that the book exists and get book
    print("user to retrieve",user_name)

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    # Create review
    review = Review(book, review_text, rating, user_name)

    # add review to user,
    user.add_review(review)

    # Update the repository dict
    # dict format{"book_id":[review]}
    repo.add_review(review)