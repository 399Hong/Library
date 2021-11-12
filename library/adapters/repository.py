import abc
from typing import List
from datetime import date
from typing import Union
from library.domain.model import *


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_book(self,book:Book):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        """ Returns the User named user_name from the repository.
        If there is no User with the given user_name, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_book_dict(self, book: Book):
        """" Adds a book to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_book(self)-> Book:
        raise NotImplementedError
        
    @abc.abstractmethod
    def get_book(self, id:int) -> Book:
        """ Returns the book with id from the repository.
        If there is no books with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_book(self) -> Book:
        # for testing purpose
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_by_bulk(self,currentPos:int, size : int) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_year(self,year:int) -> list:
        raise NotImplementedError
    
    @abc.abstractmethod
    def search_by_author(self,author:str) -> list:
        raise NotImplementedError
        
    @abc.abstractmethod
    def search_by_publisher(self,publisher:str) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def search_by_publisher(self,publisher:str) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        if not isinstance(review, Review):
            raise RepositoryException('variable review does not contain a Review object')
        if review.book is None:
            raise RepositoryException('Review not correctly attached to an book')
    

    @abc.abstractmethod
    def get_reviews_by_id(self,id:int) ->  Union[list,None]:
        """ Returns the reviews stored in the repository. """
        raise NotImplementedError



'''
class AbstractRepository(abc.ABC):


    @abc.abstractmethod
    def add_article(self, article: Article):
        """ Adds an Article to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_article(self, id: int) -> Article:
        """ Returns Article with id from the repository.
        If there is no Article with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_articles_by_date(self, target_date: date) -> List[Article]:
        """ Returns a list of Articles that were published on target_date.
        If there are no Articles on the given date, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_articles(self) -> int:
        """ Returns the number of Articles in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_article(self) -> Article:
        """ Returns the first Article, ordered by date, from the repository.
        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_article(self) -> Article:
        """ Returns the last Article, ordered by date, from the repository.
        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_articles_by_id(self, id_list):
        """ Returns a list of Articles, whose ids match those in id_list, from the repository.
        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_article_ids_for_tag(self, tag_name: str):
        """ Returns a list of ids representing Articles that are tagged by tag_name.
        If there are Articles that are tagged by tag_name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_date_of_previous_article(self, article: Article):
        """ Returns the date of an Article that immediately precedes article.
        If article is the first Article in the repository, this method returns None because there are no Articles
        on a previous date.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_date_of_next_article(self, article: Article):
        """ Returns the date of an Article that immediately follows article.
        If article is the last Article in the repository, this method returns None because there are no Articles
        on a later date.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_tag(self, tag: Tag):
        """ Adds a Tag to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tags(self) -> List[Tag]:
        """ Returns the Tags stored in the repository. """
        raise NotImplementedError

    '''