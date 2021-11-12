from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey, Boolean
)
from sqlalchemy.orm import mapper, relationship, synonym

from library.domain import model

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
    #reviews added in mapper DONE
)
#TBD
reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', ForeignKey('users.user_name')),
    Column('book_id', ForeignKey('books.id')),
    Column('review_text', String(1024), nullable=False),
    Column('rating',Integer,nullable = False),
    Column('timestamp', String(255), nullable=False)
    ## TBD add relation to book
)

books_table = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    #Column('book_id',Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('description', String(1024)), #nullable=False),
    Column('release_year', Integer), #nullable=False),
    Column('publisher_id',ForeignKey("publishers.id")),#nullable=False),
    #Column('author_id',ForeignKey("authors.id")),#????
    # may be the other way around?
    Column('cover_url', String(255))

    #add author relationship???
)

authors_table = Table(
    'authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)

publishers_table = Table(
    'publishers', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255),unique=True),
  


)
book_authors_table = Table(
    'book_authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.id')),
    Column('author_id', ForeignKey('authors.id'))

)


def map_model_to_tables():
    mapper(model.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(model.Review) #, backref='_Review__userName')
        # this could be a potential problem
    })
    mapper(model.Review, reviews_table, properties={
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__rating': reviews_table.c.rating,
        '_Review__timestamp': reviews_table.c.timestamp,
        '_Review__userName': reviews_table.c.user_name,

        '_Review__book': relationship(model.Book)
        # this could be a potential problem
    })
    mapper(model.Book, books_table, properties={
        '_Book__book_id': books_table.c.id,
        '_Book__title': books_table.c.title,
        '_Book__description': books_table.c.description,
        '_Book__release_year': books_table.c.release_year,
        '_Book__cover_url': books_table.c.cover_url,

        '_Book__authors': relationship(model.Author,secondary=book_authors_table),
                                    
        
        '_Book__publisher': relationship(model.Publisher),
    })
    mapper(model.Author, authors_table, properties={
        '_Author__unique_id': authors_table.c.id,
        '_Author__full_name': authors_table.c.name,
        
    })
    mapper(model.Publisher, publishers_table, properties={
        '_Publisher__name': publishers_table.c.name,

    })