#!/usr/bin/env python3
import sys
import re
from importlib import metadata
from . import notedb as db
from . import console_output as cons


def main():
    ## no args - list notes ##
    if len(sys.argv) == 1:
        # read database contents and write out to console
        # ( ignore :later: tagged notes )
        current_notes = db.get_tag_unmatches('later')

        for note in current_notes:
            cons.send_note(note)

        return


    ## version ##
    version_flags = ('-version', '--version')

    if sys.argv[1] in version_flags:
        cons.send_version(metadata.version("note"))
        return


    ## list notes ##
    list_flags = (
        '-l', 'l', '-ls', 'ls',
        '-list', '--list', 'list',
    )

    if sys.argv[1] in list_flags:
        # read database contents and write out to console
        notes = db.get_notes()

        for note in notes:
            cons.send_note(note)

        return


    ## clear (remove all) notes ##
    clear_flags = (
        '-clear', '--clear',
        '-reset', '--reset',
        '-remove-all', '--remove-all',
    )

    if sys.argv[1] in clear_flags:
        db.clear_database()
        return


    ## delete note(s) ##
    delete_flags = (
        '-d', 'd', '-delete', '--delete', 'delete',
        '-rm', 'rm', '-remove', '--remove', 'remove',
        '-complete', '--complete', 'complete',
        '-done', '--done', 'done',
        '-drop', '--drop', 'drop',
    )

    if sys.argv[1] in delete_flags:
        # delete selected database entries
        note_ids = sys.argv[2:]

        notes = db.get_notes(note_ids)

        db.delete_entries(note_ids)

        for note in notes:
            cons.send_confirmation(note, "done")

        return


    ## search (general) ##
    message_search_flags = (
        '-s', 's', '-search', '--search', 'search',
        '-f', '-fd', 'fd', '-find', '--find', 'find',
        '-filter', '--filter', 'filter',
    )

    if sys.argv[1] in message_search_flags:
        # search database and output results
        match = sys.argv[2]

        search_matches = db.get_note_matches(match)

        for note in search_matches:
            cons.send_note(note)

        return
        

    ## tag search ##
    tag_search_flags = ('-t', 't', '-tag', '--tag', 'tag')

    if sys.argv[1] in tag_search_flags:
        # search database for tags and output results
        tag = sys.argv[2]

        search_matches = db.get_tag_matches(tag)

        for note in search_matches:
            cons.send_note(note)

        return


    ## update note ##
    update_flags = (
        '-u', 'u', '-update', '--update', 'update',
        '-e', 'e', '-edit', '--edit', 'edit',
    )

    if sys.argv[1] in update_flags:
        note_id = sys.argv[2]
        message = sys.argv[3]

        db.update_entry(note_id, message)

        # read note back from database and send confirmation
        note = db.get_notes(note_id)[0]
        cons.send_confirmation(note, "updated")

        return


    ## append note ##
    append_flags = ('-append', '--append', 'append')

    if sys.argv[1] in append_flags:
        note_id = sys.argv[2]
        s = sys.argv[3]

        # retrieve note
        nid, dt, msg = db.get_notes(note_id)[0]

        # update note with appended message
        db.update_entry(note_id, msg + ' ' + s)

        # read note back from database and send confirmation
        note = db.get_notes(note_id)[0]
        cons.send_confirmation(note, "appended")

        return


    ## rebase notes ##
    rebase_flags = ('-rebase', '--rebase', 'rebase')

    if sys.argv[1] in rebase_flags:
        # update database nids
        db.rebase()
        return


    ## add notes ##
    add_flags = (
        '-a', 'a',
        '-add', '--add', 'add',
    )

    if sys.argv[1] in add_flags:
        # load notes into database
        add_notes = sys.argv[2:]

        db.add_entries(add_notes)

        # read notes back from database and send confirmation

        db_notes = []
        for note in add_notes:
            db_notes += db.get_note_matches(note)

        disp_notes = sorted(
            db_notes,
            key=lambda tup: tup[0],
            reverse=True, # current addition(s) at top
        )[:len(add_notes)] # grab same number as added

        for note in reversed(disp_notes):
            cons.send_confirmation(note, "added")

        return


    ## check for unknown option ##
    cons.send_option_unknown(sys.argv[1])




if __name__ == "__main__":
    main()
