
from pathlib import Path
from datetime import date, datetime
from typing import List
from typing import Union

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from library.adapters.repository import AbstractRepository, RepositoryException
from library.domain.model import *
from library.adapters.jsondatareader import BooksJSONReader

import utils

class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__books = list()
        self.__books_id = dict()
        #self.__tags = list()
        self.__users = list()
        self.__reviews = dict()


    @property
    def books(self):
        return self.__books

    @books.setter
    def books(self,books:list):
        self.__books = books  

    def add_book(self,book:Book):

        if isinstance(book, Book):
            self.__books.append(book)
        else:
            raise RepositoryException("Add a non book type to the repo")

    def add_user(self, user: User):
        
        self.__users.append(user)
        print("***User added**",self.__users)

    def get_user(self, user_name) -> User:
        print("reviews!!::::",self.__reviews)
        for user in self.__users:

            if user.user_name == user_name:
              
                return user
        return None

    def add_book_dict(self, book: Book):
        if book.book_id in self.__books_id:
           raise RepositoryException("Waring! Trying to add book with the same ID")
        
        self.__books_id[book.book_id] = book
        

    def get_first_book(self)-> Book:
        '''      
        This function is for testing purpose.no error handling code for empty list
        @return the first book
        '''
        return self.__books[0]

    def get_book(self, id: int) -> Book:
        book = None

        try:
            #book_index is a dict
            book = self.__books_id[id]
        except KeyError:
            pass  # Ignore exception and return None.

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
        numBooks = len(self.__books)
        newPos = currentPos+size

        if currentPos > numBooks:
            raise RepositoryException("Exceed book limits in memory_repository get_book_by_bulk")

        if newPos < numBooks:
            #if there is enough book to display
            nextBatch  = True

            return (newPos,nextBatch,self.__books[currentPos:newPos])
        elif newPos >= numBooks:

            newPos = numBooks
            nextBatch  = False
            return (newPos,nextBatch,self.__books[currentPos:])

    def search_by_year(self,year:int) -> list:
        matchedBook = []
        if not isinstance(year, int):
            #invalid input, return nothing
            return matchedBook

        for book in self.__books:
            if book.release_year == year:
                matchedBook.append(book)
        return matchedBook

    
    def search_by_author(self,author:str,simiarity:float = 0.5) -> list:
        matchedBook = []
        if not isinstance(author, str):
            #invalid input, return nothing
            return matchedBook
        for book in self.__books:
            for ele in book.authors:
                if utils.similar(ele.full_name, author) > simiarity:
                    matchedBook.append(book)
                    break
        return matchedBook
    
        
    def search_by_publisher(self,publisher:str,simiarity:float = 0.5) -> list:
        matchedBook = []
        if not isinstance(publisher, str):
            #invalid input, return nothing
            return matchedBook
        for book in self.__books:
                print(book.publisher)
                if utils.similar(book.publisher.name, publisher) > simiarity:
                    matchedBook.append(book)
        return matchedBook

    def add_review(self, review: Review):
        # TBT
        super().add_review(review) # check for the existence of the book that the review belongs

        id = review.book.book_id
        self.__reviews.setdefault(id,[]).append(review)
       
    def get_reviews_by_id(self, id : int) -> Union[list,None]:
        # TBT
        reviews = None
        try:
            reviews = self.__reviews[id]
        except KeyError:
            pass
        return reviews
        
def load_books(books:list,repo:MemoryRepository):
    repo.books = books

def load_books_dict(repo:MemoryRepository):
    # TBT
    for b in repo.books:
        repo.add_book_dict(b)
    

    
def populate(p: Path, repo: MemoryRepository):
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
