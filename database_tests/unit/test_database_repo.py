from pathlib import Path
import pytest

from utils import get_project_root

from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory
from library.adapters.jsondatareader import BooksJSONReader
from library.adapters.repository import AbstractRepository, RepositoryException
from library.adapters.database_repository import *

class  TestRepo:

    def test_loadBook(self,session_factory):

        repo = SqlAlchemyRepository(session_factory)
        assert type(repo.get_first_book()) == Book


    def test_add_book_dict_valid(self,session_factory):
        repo = SqlAlchemyRepository(session_factory)
        book = repo.get_book(35452242)
        assert book.title == "Bounty Hunter 4/3: My Life in Combat from Marine Scout Sniper to MARSOC"

    def test_add_book_dict_invalid(self,session_factory):
        repo = SqlAlchemyRepository(session_factory)
        book = repo.get_book("ds")
        assert book == None

    def test_get_book_by_bulk_start(self,session_factory):
        #testing from the first book
        repo = SqlAlchemyRepository(session_factory)
        newPos,nextBatch,bulkBooks = repo.get_book_by_bulk(0, 20)
        assert(newPos == 20 and nextBatch == False and bulkBooks != [])


    def test_get_book_by_bulk_Nonexistence_limit(self,session_factory):
        #testing for books that doesnt exist, currentPos is not valid
        repo = SqlAlchemyRepository(session_factory)
        try :
            newPos,nextBatch,bulkBooks = repo.get_book_by_bulk(200, 20)
        except RepositoryException:
            assert True


    def test_get_book_by_bulk_last_batch_limit(self,session_factory):
        #testing for last batch of the book
        repo = SqlAlchemyRepository(session_factory)
        numsBooks = 20
        newPos,nextBatch,bulkBooks = repo.get_book_by_bulk(numsBooks-1, 5)
        assert(newPos == 20 and nextBatch == False and bulkBooks != [])

    def test_search_by_year_valid_input(self,session_factory):
        repo = SqlAlchemyRepository(session_factory)
        books = repo.search_by_year(2016)
        assert len(books) == 5

    def test_search_by_year_valid_input_NoMatch(self,session_factory):
        repo = SqlAlchemyRepository(session_factory)
        books = repo.search_by_year(0000)
        assert len(books) == 0

    def test_search_by_year_invalid_input(self,session_factory):
        repo = SqlAlchemyRepository(session_factory)
        books = repo.search_by_year("abcd")
        assert len(books) == 0

    def test_search_by_author_valid_input(self,session_factory):
        repo = SqlAlchemyRepository(session_factory)
        books = repo.search_by_author("Takashi")
        assert len(books)==1

    def test_search_by_author_invalid_input(self,session_factory):
        repo = SqlAlchemyRepository(session_factory)
        books = repo.search_by_author(23123)
        assert len(books)==0

    def test_search_by_publisher_valid_input(self,session_factory):
        repo = SqlAlchemyRepository(session_factory)
        books = repo.search_by_publisher("Dynamite")
        assert len(books)==1
 
        
    def test_search_by_publisher_invalid_input(self,session_factory):
        repo = SqlAlchemyRepository(session_factory)
        books = repo.search_by_publisher(2332)
        assert len(books)==0
    
    # tese add_review function
    def test_add_review_valid_review(self,session_factory):
        repo = SqlAlchemyRepository(session_factory)
        book = Book(123321,"test Book")
        review = Review(book, "this is a test review", 5)
        try:
            repo.add_review(review)
            assert True
        except:
            assert False

    def test_add_review_invalid_review(self,session_factory):
        repo = SqlAlchemyRepository(session_factory)

        book = Book(123321,"test Book")
        review = Review(book, "this is a test review", 5)
        try :
            repo.add_review(None)
            assert False
        except RepositoryException:
            assert True

    def test_add_review_invalid_no_book_attached_to_review(self,session_factory):
        repo = SqlAlchemyRepository(session_factory)
        book = Book(123321,"test Book")
        review = Review(None, "this is a test review", 5)
        try :
            repo.add_review(review)
            assert False
        except RepositoryException:
            assert True
    #test get review by id function
    def test_get_review_by_id_valid(self,session_factory):
        repo = SqlAlchemyRepository(session_factory)
        book = Book(123321,"test Book")
        review = Review(book, "this is a test review", 5)
        repo.add_review(review)
        review = repo.get_reviews_by_id(123321)
        assert len(review) == 1

    def test_get_review_by_id_invalid(self,session_factory):
        repo = SqlAlchemyRepository(session_factory)

        book = Book(123321,"test Book")
        review = Review(book, "this is a test review", 5)
        repo.add_review(review)
        review = repo.get_reviews_by_id("123")
        print(review)
        assert review == None
        review = repo.get_reviews_by_id(1234)
        assert review == None
        


        