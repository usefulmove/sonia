#!/usr/bin/env python3
import sys
import duckdb
from importlib import metadata
from . import notedb as db


def main():
    ## no args - list notes
    if len(sys.argv) == 1:
        sys.argv += ['-list']


    ## version
    if sys.argv[1] in ('-version', '--version'):
        print(f'  note {metadata.version("note")}')
        return


    ## list notes
    if sys.argv[1] in ('-l', '-ls', '-list', '--list'):
        # read database contents and write out to console
        notes = db.get_notes()

        print()
        for e in notes:
            print(f'  {e[1].strftime("%y.%m.%d %H:%M")} | {e[0]} | {e[2]}')
        print()

        return


    ## clear notes
    if sys.argv[1] in ('-clear', '--clear', '-reset', '--reset'):
        db.clear_database()
        return


    ## delete note(s)
    if sys.argv[1] in ('-d', '-delete', '--delete', '-rm'):
        # delete selected database entries
        note_ids = sys.argv[2:]
        db.delete_entries(note_ids)
        return


    ## search (general)
    if sys.argv[1] in ('-s', '-search', '--search', '-f', '-fd', '-find', '--find', '-filter', '--filter'):
        # search database and output results
        match = sys.argv[2]

        search_matches = db.get_note_matches(match)

        print()
        for e in search_matches:
            print(f'  {e[1].strftime("%y.%m.%d %H:%M")} | {e[0]} | {e[2]}')
        print()

        return
        

    ## tag search
    if sys.argv[1] in ('-t', '-tag', '--tag'):
        # search database for tags and output results
        tag = sys.argv[2]

        search_matches = db.get_tag_matches(tag)

        print()
        for e in search_matches:
            print(f'  {e[1].strftime("%y.%m.%d %H:%M")} | {e[0]} | {e[2]}')
        print()

        return


    ## update note
    if sys.argv[1] in ('-u', '-update', '--update', '-e', '-edit', '--edit'):
        note_id = sys.argv[2]
        message = sys.argv[3]

        db.update_entry(note_id, message)

        return


    ## rebase notes
    if sys.argv[1] in ('-rebase', '--rebase'):
        # update database nids
        db.rebase()
        return


    ## check for unknown option
    if sys.argv[1].startswith('-'):
        print(f'  note: unknown option ({sys.argv[1]})')
        return


    ## otherwise add notes
    # load notes into database
    notes = sys.argv[1:]

    db.add_entries(notes)

    # display confirmation message
    print()
    for note in notes:
        print(f'  {note} | ( added )')
    print()




if __name__ == "__main__":
    main()
