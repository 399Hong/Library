from datetime import date

import pytest

from library.authentication.service import AuthenticationException
from library.browse import service as browse_services
from library.authentication import service as auth_services
from library.search import service as search_services
from library.addBook import service as addBook_services
from library.browse.service import NonExistentBookException, UnknownUserException
from library.domain.model import *
from library.adapters.repository import AbstractRepository, RepositoryException

def test_can_add_user(in_memory_repo):
    new_user_name = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = 'thorke'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)
    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)


def test_can_add_get_review(in_memory_repo):
    id = 35452242
    rating = 3
    review_text = 'The loonies are stripping the supermarkets bare!'
    user_name = 'pmccartney'
    password = 'abcd1A23'

    auth_services.add_user(user_name, password, in_memory_repo)

    # Call the service layer to add the book.
    browse_services.add_review(user_name, id, review_text, rating, in_memory_repo)

    # Retrieve the comments for the book from the repository.
    reviews = browse_services.get_reviews_for_book(id, in_memory_repo)
    # Check that the reviews include a review with the new comment text.
    assert len(reviews) == 1
    review = reviews.pop()
    assert review.review_text == review_text
    assert review.rating == rating


def test_cannot_add_review_for_non_existent_article(in_memory_repo):
    id = 99999
    review_text = "This is test"
    user_name = 'fmercury'
    password = 'abcd1A23'
    rating = 3

    auth_services.add_user(user_name, password, in_memory_repo)

    with pytest.raises(NonExistentBookException):
        browse_services.add_review(user_name, id, review_text, rating, in_memory_repo)



def test_cannot_add_comment_by_unknown_user(in_memory_repo):
    id = 35452242
    review_text = 'The loonies are stripping the supermarkets bare!'
    user_name = 'hhong'
    rating = 5

    # Call the service layer to attempt to add the comment.
    with pytest.raises(UnknownUserException):
        browse_services.add_review(user_name, id, review_text, rating, in_memory_repo)


def test_get_book_bulk_valid_input(in_memory_repo):

    newPos,nextBatch,bulkBooks = browse_services.get_book_bulk(0,20,in_memory_repo)
    assert(newPos == 20 and nextBatch == False and bulkBooks != [])

def test_get_book_bulk__Nonexistence_limit(in_memory_repo):
    try :
        newPos,nextBatch,bulkBooks = browse_services.get_book_bulk(200, 20,in_memory_repo)
    except:
        assert True

def test_get_book_bulk_last_batch_limit(in_memory_repo):

    numsBooks = len(in_memory_repo.books)
    newPos,nextBatch,bulkBooks = browse_services.get_book_bulk(numsBooks-1,5,in_memory_repo)
    assert(newPos == 20 and nextBatch == False and bulkBooks != [])

def test_get_book_by_id(in_memory_repo):
    id = 35452242
    book = browse_services.get_book_by_id(id,in_memory_repo)
    assert isinstance(book, Book)

def test_get_book_by_id(in_memory_repo):
    id = 354522422333
    with pytest.raises(NonExistentBookException):
        book = browse_services.get_book_by_id(id,in_memory_repo)
  
def test_find_books_by_year_valid(in_memory_repo):
    books = search_services.find_books_by_year(2016, in_memory_repo)
    assert len(books) == 5
def test_find_books_by_year_valid_no_book(in_memory_repo):
    books = search_services.find_books_by_year(2017, in_memory_repo)
    assert len(books) == 0
def test_find_books_by_year_invalid(in_memory_repo):
    books = search_services.find_books_by_year("", in_memory_repo)
    assert len(books) == 0

def test_find_books_by_author_valid(in_memory_repo):
    books = search_services.find_books_by_author("Garth", in_memory_repo)
    assert len(books) == 2
def test_find_books_by_author_valid_no_book(in_memory_repo):
    books = search_services.find_books_by_author(123, in_memory_repo)
    assert len(books) == 0
def test_find_books_by_author_invalid(in_memory_repo):
    books = search_services.find_books_by_author("", in_memory_repo)
    assert len(books) == 0

def test_find_books_by_publisher_valid(in_memory_repo):
    books = search_services.find_books_by_publisher("Avatar", in_memory_repo)
    assert len(books) == 4
def test_find_books_by_publisher_valid_no_book(in_memory_repo):
    books = search_services.find_books_by_publisher(123, in_memory_repo)
    assert len(books) == 0
def test_find_books_by_publisher_invalid(in_memory_repo):
    books = search_services.find_books_by_publisher("", in_memory_repo)
    assert len(books) == 0

def test_create_author():
    author = addBook_services.create_author("123431")
    assert isinstance(author, Author)
def test_create_book():
    book = addBook_services.create_new_book(123321, "This is a test", "This is a test", "This is a test", 1999)
    assert isinstance(book,Book)

def test_create_book_invalid_id():
    try:
        book = addBook_services.create_new_book("123", "This is a test", "This is a test", "This is a test", 1999)
        assert False
    except ValueError:
        assert True
def test_load_new_book(in_memory_repo):
    addBook_services.load_new_book_into_repo(12331, "This is a test", "This is a test", "This is a test", 199, in_memory_repo)
    book = in_memory_repo.get_book(12331)
    assert book.title == "This is a test"

def test_load_new_book_duplicateKey(in_memory_repo):
    with pytest.raises(RepositoryException):
        addBook_services.load_new_book_into_repo(12331, "This is a test", "This is a test", "This is a test", 199, in_memory_repo)
        addBook_services.load_new_book_into_repo(12331, "This is a test", "This is a test", "This is a test", 199, in_memory_repo)
        book = in_memory_repo.get_book(12331)

