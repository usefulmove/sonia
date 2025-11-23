#!/usr/bin/env python3
import sys
from note import console_output as cons
from note import notedb as db
from note import commands as cmd


def main() -> None:
    if not db.PRODUCTION:
        cons.send_warning('running in TEST mode')


    ## no args - run short list command ##
    if len(sys.argv) < 2:
        cmd.commands['shortls'].run()
        return


    ## command execution ##
    cmd_id: str = sys.argv[1]

    if cmd_id in cmd.commands:
        cmd.commands[cmd_id].run()
        return

    ## unknown command ##
    cons.send_error('unknown command', cmd_id)


if __name__ == "__main__":
    main()
