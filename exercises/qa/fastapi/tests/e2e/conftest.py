import pathlib
import psycopg2
import pytest

from requests import Session
from urllib.parse import urljoin

# would be better off in a config file if this was a real project
base_url = "http://localhost:8000"


class Api(Session):
    """
    Custom requests session that prepends the base URL to all requests
    """
    def __init__(self) -> None:
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, *args, **kwargs):
      joined_url = urljoin(self.base_url, url)
      return super().request(method, joined_url, *args, **kwargs)


@pytest.fixture(scope="session")
def api(db):
    """
    Fixture that we use instead of calling methods on the requests module directly.

    Allows us to set up and clean up the database for each test run.
    """
    yield Api()



@pytest.fixture(scope="session")
def db():
  """
  This fixture uses psycopg2 to create a connection to the database.
  It then reads and executes the SQL file to create the table data.

  When the test session is over, it truncates the table data.
  """
  conn = psycopg2.connect(
    dbname="testdb",
    user="admin",
    password="1234",
    host="localhost",
    port="5432"
  )
  conn.autocommit = True
  cursor = conn.cursor()

  # get the path to this file and work out the location of the seed file
  tests_folder = pathlib.Path(__file__).parent.parent.resolve()
  db_seed_file = pathlib.Path(tests_folder, "data/tasks-seed.sql")

  with open(db_seed_file) as f:
    cursor.execute(f.read())

  yield conn

  cursor.execute("TRUNCATE TABLE tasks")