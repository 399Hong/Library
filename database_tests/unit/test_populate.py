from sqlalchemy import select, inspect

from library.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)

    assert inspector.get_table_names() == ['authors', 'book_authors', 'books', 'publishers', 'reviews', 'users']

def test_database_populate_select_all_authors(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_authors_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_authors_table]])
        result = connection.execute(select_statement)

        all_authors_names = []
        for row in result:
            all_authors_names.append(row['name'])

        assert all_authors_names == ['Garth Ennis', 'Mike Wolfer', 'Dan Slott', 'Ed Brubaker', 'Scott Beatty', 'Andrea DiVito', 'Jerry Siegel', 'Joe Shuster', 'Rich Tommaso', 'Keith Burns', 'Kieron Dwyer', 'Naoki Urasawa', 'Katsura Hoshino', 'Maki Minami', 'Chris  Martin', 'Yuu Asami', 'Rafael Ortiz', 'Tomas Aira', 'Florence Dupre la Tour', 'Jaymes Reed', 'Jeon Geuk-Jin', 'Daniel Indro', 'DigiKore Studios', 'Asma', 'Takashi   Murakami', 'Cun Shang Chong', 'Matt Martin', 'Fernando Heinz', 'Lindsey Schussman', 'Simon Spurrier', 'Jason Delgado']

def test_database_populate_select_all_book_authors(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[table]])
        result = connection.execute(select_statement)

        allData= []
        for row in result:
            allData.append(row['book_id'])
        
        assert allData == [25742454, 30128855, 13571772, 35452242, 35452242, 707611, 707611, 2250580, 27036536, 27036536, 27036536, 27036536, 27036537, 27036538, 27036538, 27036538, 27036538, 27036538, 27036539, 27036539, 23272155, 11827783, 11827783, 12349665, 12349663, 30735315, 17405342, 13340336, 18711343, 18711343, 18711343, 2168737, 2168737, 2168737, 18955715]

def test_database_populate_select_all_books(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[table]])
        result = connection.execute(select_statement)

        allData= []
        for row in result:
            allData.append(row['id'])
        
        assert allData == [707611, 2168737, 2250580, 11827783, 12349663, 12349665, 13340336, 13571772, 17405342, 18711343, 18955715, 23272155, 25742454, 27036536, 27036537, 27036538, 27036539, 30128855, 30735315, 35452242]

def test_database_populate_select_all_publishers(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[table]])
        result = connection.execute(select_statement)

        allData= []
        for row in result:
            allData.append(row['name'])
        assert allData == ['N/A', 'Dargaud', 'Hachette Partworks Ltd.', 'DC Comics', 'Go! Comi', 'Avatar Press', 'Dynamite Entertainment', 'VIZ Media', 'Hakusensha', 'Planeta DeAgostini', 'Shi Bao Wen Hua Chu Ban Qi Ye Gu Fen You Xian Gong Si', 'Marvel']

def test_database_populate_select_all_reviews(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[table]])
        result = connection.execute(select_statement)

        allData= []
        for row in result:
            allData.append(row['id'])
        assert allData == []
def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[table]])
        result = connection.execute(select_statement)

        allData= []
        for row in result:
            allData.append(row['id'])
        assert allData == []