#!/usr/bin/env python3
import sys
from sonia import console_output as cons
from sonia import commands as cmd


def main() -> None:
    match sys.argv:
        case _, cmd_id, *args if cmd_id in cmd.commands:
            cmd.commands[cmd_id].run(tuple(args))
        case [_]: # no args
            cmd.commands['focus'].run()
        case _, unknown, *_: 
            cons.send_error('unknown command', unknown)


if __name__ == "__main__":
    main()
