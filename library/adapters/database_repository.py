from datetime import date
from typing import List
from typing import List
from typing import Union
from pathlib import Path

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from library.domain.model import *
from library.adapters.repository import AbstractRepository, RepositoryException
from library.adapters.jsondatareader import BooksJSONReader
import utils

from library.adapters.orm import metadata as md

class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # start here
    def add_book(self,book:Book):
        #additional check for user added book
        authors = book.authors
        if len(book.authors)==1:
           
            existedAuthor = self._session_cm.session.query(Author).filter(Author._Author__full_name == authors[0].full_name).first()
            
            if existedAuthor != None:
                book.remove_author(authors[0])
                book.add_author(existedAuthor)

        
        with self._session_cm as scm:
            scm.session.add(book)
            scm.commit()



    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_book_dict(self, book: Book):
        pass
        

    def get_first_book(self)-> Book:
        '''      
        This function is for testing purpose.no error handling code for empty list
        @return the first book
        '''
        book = None

        book = self._session_cm.session.query(Book).first()
        return book
        

    def get_book(self, id: int) -> Book:
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__book_id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return book

    def get_book_by_bulk(self,currentPos:int, size : int ) -> list:
        """
        @param
        currentPos: the last book(position) on display
        size: number of books to display

        @return
        a tuple
        1. the new last book after taking the batch
        2. availability of next batch
        3. a list contains the books retrieved for display

        """
        #TBD need to be unit tested

        books = None
        try:
            books = self._session_cm.session.query(Book).all()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        numBooks = len(books)
        newPos = currentPos+size

        if currentPos > numBooks:
            raise RepositoryException("Exceed book limits in memory_repository get_book_by_bulk")

        if newPos < numBooks:
            #if there is enough book to display
            nextBatch  = True

            return (newPos,nextBatch,books[currentPos:newPos])
        elif newPos >= numBooks:

            newPos = numBooks
            nextBatch  = False
            return (newPos,nextBatch,books[currentPos:])

    def search_by_year(self,year:int) -> list:

        books = None
        try:
            books = self._session_cm.session.query(Book).all()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        matchedBook = []
        if not isinstance(year, int):
            #invalid input, return nothing
            return matchedBook

        for book in books:
            if book.release_year == year:
                matchedBook.append(book)
        return matchedBook

    
    def search_by_author(self,author:str,simiarity:float = 0.5) -> list:

        books = None
        try:
            books = self._session_cm.session.query(Book).all()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        matchedBook = []
        if not isinstance(author, str):
            #invalid input, return nothing
            return matchedBook
        for book in books:
            for ele in book.authors:
                if utils.similar(ele.full_name, author) > simiarity:
                    matchedBook.append(book)
                    break
        return matchedBook
    
        
    def search_by_publisher(self,publisher:str,simiarity:float = 0.5) -> list:
        books = None
        try:
            books = self._session_cm.session.query(Book).all()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        matchedBook = []
        if not isinstance(publisher, str):
            #invalid input, return nothing
            return matchedBook

        for book in books:
                if book.publisher == None:
                    continue
                if utils.similar(book.publisher.name, publisher) > simiarity:
                    matchedBook.append(book)
        return matchedBook
#TBD
    def add_review(self, review: Review):
        # TBT
        super().add_review(review) # check for the existence of the book that the review belongs

        id = review.book.book_id
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()
       
    def get_reviews_by_id(self, id : int) -> Union[list,None]:
        # TBT
        reviews = None
        try:
            reviews = self._session_cm.session.query(Review).filter(md.tables["reviews"].c.book_id == id).all()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        if reviews == []:
            reviews = None
        return reviews

def load_books(books:list,repo:SqlAlchemyRepository):
    for book in books:
        repo.add_book(book)

def load_books_dict(repo:SqlAlchemyRepository):
    # TBT
   pass
    

    
def database_populate(p: Path, repo: SqlAlchemyRepository):
    # read in  a list of books 
    dataFolder = "library/adapters/data/"
    bookFile = "comic_books_excerpt.json"
    authorFile = "book_authors_excerpt.json"

    #object that can read in the data
    books = BooksJSONReader(p/dataFolder/bookFile,p/dataFolder/authorFile)
    # reading in a list of books to the repo
    books.read_json_files()
    load_books(books.dataset_of_books, repo)

    load_books_dict(repo)