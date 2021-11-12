from library.adapters.repository import AbstractRepository
#import library.adapters.repository as repo
from library.domain.model import Book, Review, Author
from typing import Union


def load_new_book_into_repo(book_id: int, title:str, desc: str,author:str,year:int,repo:AbstractRepository):
    book = create_new_book(book_id, title, desc, author, year)
    repo.add_book(book)
    repo.add_book_dict(book)


def create_new_book(book_id: int, title:str, desc: str,author:str,year:int):
    book = Book(book_id,title)
    book.release_year = int(year)
    book.description = desc
    book.add_author(create_author(author))
    book.cover_url = "https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png"
    return book

def create_author(author:str) -> Author:
    id = int(''.join([str(ord(l)) for l in author]))
    return Author(id,author)

    