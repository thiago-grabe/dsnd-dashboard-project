import pytest
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent


@pytest.fixture
def db_path():
    """
    Return the path to the database file.

    The database file is expected to be located at
    `python-package/employee_events/employee_events.db`. If the file does not
    exist, the test will fail.
    """
    return project_root / "python-package" / "employee_events" / "employee_events.db"


def test_db_exists(db_path):
    """
    Verify that the database file exists.

    The database file is expected to be located at
    `python-package/employee_events/employee_events.db`. If the file does not
    exist, the test will fail.
    """
    
    assert db_path.is_file(), f"The database file does not exist: {db_path}"


@pytest.fixture
def db_conn(db_path):
    """
    Return a connection to the SQLite database.

    The database connection is created using the path given by the
    `db_path` fixture. This fixture is intended to be used by tests
    that need to access the database.

    Returns:
        sqlite3.Connection: A connection to the SQLite database
    """
    from sqlite3 import connect

    return connect(db_path)


@pytest.fixture
def table_names(db_conn):
    """
    Retrieve a list of table names in the SQLite database.

    This fixture uses the `db_conn` fixture to execute a query on the
    SQLite database. It selects the names of all tables present in the
    database and returns them as a list of strings.

    Args:
        db_conn (sqlite3.Connection): A connection to the SQLite database.

    Returns:
        List[str]: A list of table names present in the database.
    """

    name_tuples = db_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()
    return [x[0] for x in name_tuples]


def test_employee_table_exists(table_names):
    """
    Verify that the 'employee' table exists in the database.

    This test function receives the `table_names` fixture as an argument.
    It asserts that the string 'employee' is in the list of table names,
    indicating that the 'employee' table exists in the database.
    """
    assert "employee" in table_names, "Table 'employee' does not exist in the database"


def test_team_table_exists(table_names):
    """
    Verify that the 'team' table exists in the database.

    This test function receives the `table_names` fixture as an argument.
    It asserts that the string 'team' is in the list of table names,
    indicating that the 'team' table exists in the database.
    """

    assert "team" in table_names, "Table 'team' does not exist in the database"



def test_employee_events_table_exists(table_names):
    """
    Verify that the 'employee_events' table exists in the database.

    This test function receives the `table_names` fixture as an argument.
    It asserts that the string 'employee_events' is in the list of table names,
    indicating that the 'employee_events' table exists in the database.
    """
    assert (
        "employee_events" in table_names
    ), "Table 'employee_events' does not exist in the database"
