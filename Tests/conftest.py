import pytest

from CS235Flix.adapters.memory_repository import MemoryRepository, populate

# TEST_DATA_PATH = "../../../adapters/datafiles/"
# TEST_DATA_PATH = "CS235Flix/adapters/datafiles/"   # This is the path to the full 1000 movies
TEST_DATA_PATH = "Tests/data/"  # This is the path to the 10 movies


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    populate(TEST_DATA_PATH, repo)
    return repo