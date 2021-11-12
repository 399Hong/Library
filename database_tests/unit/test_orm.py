import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from library.domain.model import *


def insert_user(empty_session, values=None):
    new_name = "andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]

        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_book(empty_session):
    empty_session.execute(
        'INSERT INTO books (title, description, release_year,publisher_id, cover_url) VALUES '
        '("Test book name", '
        '"This is a test description", '
        '2021,'
        '1,'
        '"https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png")',
        
    )
    row = empty_session.execute('SELECT id from books').fetchone()
    return row[0]

def insert_author(empty_session):
    empty_session.execute(
        'INSERT INTO authors (id, name) VALUES '
        '(123321, '
        '"Test author",)'
    )
    row = empty_session.execute('SELECT id from authors').fetchone()
    return row[0]

def insert_publisher(empty_session):
    empty_session.execute(
        'INSERT INTO publishers (id, name) VALUES '
        '(121, '
        '"Test publisher",)'
    )
    row = empty_session.execute('SELECT id from publishers').fetchone()
    return row[0]




def insert_book_authors(empty_session, book_key, author_keys):
    stmt = 'INSERT INTO book_authors (book_id, author_id) VALUES (:book_id, :author_id)'

    for author_key in author_keys:
        empty_session.execute(stmt, {'book_id': book_key, 'author_id': author_key})


def insert_reviewed_book(empty_session):
    book_key = insert_book(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = "2021-10-18 18:05:19"
    timestamp_2 = "2021-10-18 18:05:38"

    empty_session.execute(
        
        'INSERT INTO reviews (user_name, book_id, review_text, rating, timestamp) VALUES '
        '(:user_id, :book_id, "review 1", 5, :timestamp_1),'
        '(:user_id, :book_id, "review 2", 4, :timestamp_2)',
        {'user_id': user_key, 'book_id': book_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT id from reviews').fetchone()
    return row[0]


def make_book():
    book = Book(
        1,
        "Test book name"
        
    )
    return book


def make_user():
    user = User("andrew", "11132312321")
    return user


def make_publisher():
    publisher = Publisher("Test publisher name")
    return publisher

def make_author():
    author = Author(11111,"Test author name")
    return author

def make_review():
    book = make_book()
    review = Review(book,"review testing",5,"testName")

def make_review(book:Book,userName:str,text:str,rating:int):
    
    return Review(book,text,rating,userName)

def test_loading_of_users(empty_session):
    users = list()
    users.append(("andrew", "1234"))
    users.append(("cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("andrew", "1234"),
        User("cindy", "999")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("andrew", "11132312321")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("andrew", "12341234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("andrew", "12341234")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_book(empty_session):
    book_key = insert_book(empty_session)
    expected_book = make_book()
    fetched_book= empty_session.query(Book).one()

    assert expected_book == fetched_book
    assert book_key == fetched_book.book_id




def test_loading_of_reviews(empty_session):
    insert_reviewed_book(empty_session)

    reviews = empty_session.query(Review).all()

    for review in reviews:
        assert review.book_id == 1


def test_saving_of_review(empty_session):
    book_key = insert_book(empty_session)
    user_key = insert_user(empty_session, ("andrew", "12341234"))

    books = empty_session.query(Book).all()
    book = books[0]
    user = empty_session.query(User).filter(User._User__user_name == "andrew").one()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    text = "Some comment text."
   
    review = make_review(book, user.user_name,text,5)


    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, book_id, review_text,rating FROM reviews'))

    assert rows == [(user.user_name, book.book_id, text,5)]


def test_saving_of_book(empty_session):
    book = make_book()
    empty_session.add(book)
    empty_session.commit()

    row = empty_session.query(Book).first()
    assert row == book

def test_saving_book_with_author(empty_session):
    author = make_author()
    #empty_session.add(author)

    book = make_book()
    book.add_author(author)

    empty_session.add(book)
    empty_session.commit()

    rows = empty_session.execute('SELECT * FROM book_authors').fetchone()
    
    assert (1, 1, 11111) == rows

def test_saving_book_with_publisher(empty_session):
    publisher = make_publisher()
    #empty_session.add(author)

    book = make_book()
    book.publisher = publisher

    empty_session.add(book)
    empty_session.commit()

    rows = empty_session.execute('SELECT * FROM publishers').fetchone()
    
    assert (1, 'Test publisher name') == rows
