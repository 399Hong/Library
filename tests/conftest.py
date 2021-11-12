import pytest

from library import create_app
from library.adapters import memory_repository
from library.adapters.memory_repository import MemoryRepository

from utils import get_project_root

TEST_DATA_PATH = get_project_root()


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo




@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })
    testClient = my_app.test_client()
    # add existing user

    testClient.post(
        '/authentication/register',
        data={'user_name': 'thorke', 'password':'abcd1A23'}
    )
    AM = auth2(testClient)
    AM.login()
    testClient.post(
        '/addComment',
        data={'review': "what is this???", 'book_id': 13571772, 'rating' : 5}
    )
    AM.logout()

    
    return testClient


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, user_name='thorke', password='abcd1A23'):
        return self.__client.post(
            'authentication/login',
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('/authentication/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)

#this is for pre-enterting some data for test purposes
def auth2(client):
    return AuthenticationManager(client)
