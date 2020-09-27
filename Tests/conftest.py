import pytest

from CS235Flix.adapters.memory_repository import MemoryRepository, populate

# TEST_DATA_PATH = "../../../adapters/datafiles/"
TEST_DATA_PATH = "CS235Flix/adapters/datafiles/"


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    populate(TEST_DATA_PATH, repo)
    return repo