import os
from collections.abc import Iterator
from pathlib import Path

import pytest
from sonia import notedb as db


test_folder = Path(__file__).parent
test_path = str(test_folder / "notedb_test.db")


entries: tuple[str, ...] = ("test_one", "test_two", "test_three")


def test_set_path() -> None:
    assert db.set_path(test_path)


def test_create_notes() -> None:
    confirmation_notes: list[db.Note] = db.create_notes(entries)

    assert len(confirmation_notes) == len(entries)


def test_is_valid() -> None:
    assert db.is_valid(len(entries))
    assert not db.is_valid(len(entries) + 1)


def test_get_notes() -> None:
    notes: list[db.Note] = db.get_notes()
    assert len(notes) == len(entries)


def test_get_note_matches() -> None:
    notes: list[db.Note] = db.get_note_matches("test")
    assert len(notes) == len(entries)


def test_get_note_unmatches() -> None:
    notes: list[db.Note] = db.get_note_unmatches("one")
    assert len(notes) == 2


def test_update_and_read_note() -> None:
    update_message = "test_one :tag:"

    db.update_note(1, update_message)

    notes: list[db.Note] = db.get_tag_matches("tag")

    assert len(notes) == 1
    assert notes[0].message == update_message


def test_get_tag_matches_unmatches() -> None:
    tag = "tag"

    matches: int = len(db.get_tag_matches(tag))
    unmatches: int = len(db.get_tag_unmatches(tag))

    assert matches != unmatches
    assert matches + unmatches == len(entries)


def test_delete_notes() -> None:
    nids: tuple[int, int] = (1, 3)

    deleted_notes: list[db.Note] = db.delete_notes(nids)

    returned_nids = tuple(note.id for note in deleted_notes)

    assert nids == returned_nids

    notes_a: list[db.Note] = db.get_notes()
    notes_b: list[db.Note] = db.get_notes((2,))

    assert notes_a == notes_b
    assert len(notes_a) == 1


def test_rebase() -> None:
    db.rebase()

    assert db.get_notes()[0].id == 1


def test_change() -> None:
    assert db.set_path(test_path)

    db.clear_database()
    db.rebase()

    db_notes = db.get_notes()

    db.create_notes(entries)

    db.change(
        (
            1,
            3,
        ),
        "test_",
        "done_",
    )
    db.change_all("_", ":")

    db_notes = db.get_notes()

    assert db_notes[0].message == "done:one"
    assert db_notes[1].message == "test:two"


def test_clear_database() -> None:
    db.clear_database()

    assert not db.get_notes()


@pytest.fixture(scope="session", autouse=True)
def cleanup_notedb_test_database() -> Iterator[None]:
    """Remove notedb test database file after tests."""
    yield
    if os.path.exists(test_path):
        os.remove(test_path)
