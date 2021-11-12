import pytest

from flask import session
from library.authentication import service as auth_services

def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('thorke', 'abcd1A23', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message,in_memory_repo):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.

    response= client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    print(response.headers['Location'])
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Library' in response.data


def test_login_required_to_comment(client):
    response = client.post('/addComment?id=707611')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_comment(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the comment page.
    response = client.get('/addComment?id=707611')

    response = client.post(
        '/addComment',
        data={'review': 'this is a test', 'book_id': 707611,'rating':5}
    )
    assert response.headers['Location'] == 'http://localhost/viewBook?id=707611&show=True'

@pytest.mark.parametrize(('review', 'messages'), (
       
        ('Hey', (b'Your comment is too short')),
        ('', (b'Your comment is too short'))
        
))
def test_review_with_invalid_input(client, auth, review, messages):
    # Login a user.
    auth.login()

    # Attempt to comment on an article.
    response = client.post(
        '/addComment',
        data={'review': review, 'book_id': 35452242, 'rating' : 5}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_get_book_without_comment(client):
    # Check that we can retrieve the articles page.
    response = client.get('/viewBook?id=13571772&show=False')
    assert response.status_code == 200

    assert b'Captain America' in response.data

def test_book_with_comment(client,auth):

    auth.login()
    # Check that we can retrieve the articles page.
    response = client.get('/viewBook?id=13571772&show=True')
    assert response.status_code == 200

    # Check that without providing a date query parameter the page includes the first article.
    
    assert b'Captain America' in response.data
    assert b"what is this???" in response.data
  


def test_search_by_year(client):

    # Check that we can retrieve the articles page.
    response = client.post(
        '/search',
        data={'search': "2016", 'searchBy' :"By release year"}
    )
    assert response.status_code == 200

    # Check that without providing a date query parameter the page includes the first article.
    print(response.data)
    assert b'Published in 2016 by Avatar Press' in response.data

def test_search_by_publisher(client):

    # Check that we can retrieve the articles page.
    response = client.post(
        '/search',
        data={'search': "Avatar Press", 'searchBy' :"By publisher name"}
    )
    assert response.status_code == 200

    # Check that without providing a date query parameter the page includes the first article.
    assert b'Avatar Press' in response.data
  
def test_search_by_author(client):

    # Check that we can retrieve the articles page.
    response = client.post(
        '/search',
        data={'search': "Garth", 'searchBy' :"By author name"}
    )
    assert response.status_code == 200

    # Check that without providing a date query parameter the page includes the first article.
    assert b'Garth' in response.data

def test_get_addBook(client,auth):
    auth.login()
    response = client.get('/addBook')
    assert response.status_code == 200
    assert b'Add a book to the Library?' in response.data

def test_get_addBook(client,auth):
    auth.login()
    response = client.get('/addBook')
    assert response.status_code == 200
    assert b'Add a book to the Library?' in response.data

def test_post_addBook(client,auth):
    auth.login()
    response = client.post(
        '/addBook',
        data={'title': "This is a test", 'Description' :"This is a test",'authorName':"This is a test","release year": 1999}
    )
    assert response.status_code == 200
    assert b"This is a test" in response.data


