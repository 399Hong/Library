"""Initialize Flask app."""

from flask import Flask, render_template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from library.adapters.memory_repository import MemoryRepository, populate
from library.adapters.database_repository import SqlAlchemyRepository, database_populate
import utils
import library.adapters.repository as repo


from library.adapters.orm import metadata, map_model_to_tables

import sys
(a,b) = sys.version_info[0:2]
# check python version
if a < 3 or b < 6:
    print("****Warining: python 3.6 is required")
    raise Exception('Requires python 3.6 and above')
else: 
    print("Python version requirement check passed")


def create_app(test_config=None):
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = MemoryRepository()
        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        database_mode = False
        """TBC"""
        #repository_populate.populate(data_path, repo.repo_instance, database_mode)

        """TBC"""
        populate(utils.get_project_root(), repo.repo_instance)

    elif app.config['REPOSITORY'] == 'database':
        # Configure database.
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        # For example the file database could be located locally and relative to the application in lib.db,
        # leading to a URI of "sqlite:///lib.db".
        # Note that create_engine does not establish any actual DB connection directly!
        database_echo = app.config['SQLALCHEMY_ECHO']
        # Please do not change the settings for connect_args and poolclass!
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()
            print("IMhere......*********************************")
            database_populate(utils.get_project_root(),repo.repo_instance)
            #repository_populate.populate(data_path, repo.repo_instance, database_mode)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()
    

    with app.app_context():
        # Register blueprints.
        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)
        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)
        from .search import search
        app.register_blueprint(search.search_blueprint)
        from .addBook import addBook
        app.register_blueprint(addBook.addBook_blueprint)
               
        # Register a callback the makes sure that database sessions are associated with http requests
        # We reset the session inside the database repository before a new flask request is generated
        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, SqlAlchemyRepository):
                repo.repo_instance.close_session()
        
    return app