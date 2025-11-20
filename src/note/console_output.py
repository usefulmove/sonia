from datetime import datetime
from rich.console import Console
import re


## rich console settings ##
console = Console()


# colors
CDIM = '#616161'
CSEP = '#454545'
CEMPH = '#faf6e4'
CNORM = 'default'


def color_tags(s: str) -> str:
    return re.sub(r":([a-z]*):", f"[{CDIM}]:\\1:[/{CDIM}]", s)


def send_version(version: str) -> None:
    console.print(f'  [{CNORM}]note[/] [{CEMPH}]{version}[/]')


def send_note(note: tuple[int, datetime, str]) -> None:
    nid, dt, msg = note

    console.print(
        f'  [{CDIM}]{dt.strftime("%y.%m.%d %H:%M")}[/]' +
        f' [{CSEP}]|[/] ' +
        f'[{CDIM}]{nid}[/]' +
        f' [{CSEP}]|[/] ' +
        f'[{CNORM}]{color_tags(msg)}[/]'
    )


def send_confirmation(note: tuple[int, datetime, str], action: str) -> None:
    nid, dt, msg = note

    console.print(
        f'  [{CNORM}]{color_tags(msg)}[/]' +
        f' [{CSEP}]|[/] ' +
        f'[{CDIM}]{nid}[/]' +
        f' [{CSEP}]|[/] ' +
        f'[{CNORM}]({action})[/]'
    )


def send_option_unknown(arg: str) -> None:
    console.print(f'  note: unknown option ([{CDIM}]{arg}[/])')
