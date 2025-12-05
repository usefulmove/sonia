import os
from sonia import notedb as db


entries: list[str] = ['test_one', 'test_two', 'test_three']
test_path = './src/sonia/test/test.db'


def test_set_path() -> None:
    assert db.set_path(test_path) == True


def test_create_notes() -> None:
    confirmation_notes: list[db.Note] = db.create_notes(entries)

    assert len(confirmation_notes) == len(entries)


def test_is_valid() -> None:
    assert db.is_valid(len(entries))
    assert not db.is_valid(len(entries) + 1)


def test_clean_up() -> None:
    # remove test database if exists
    if os.path.exists(test_path):
        os.remove(test_path)
