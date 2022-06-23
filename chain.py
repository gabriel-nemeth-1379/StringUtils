#!/usr/bin/env python3

from pathlib import Path
from typing import List, Optional
import sys


class ChainerInterface:
    def chain(self, chain: list) -> str:
        pass


class PlainChainer(ChainerInterface):
    def chain(self, chain: list) -> str:
        return ','.join(chain)


class QuotedChainer(ChainerInterface):
    def chain(self, chain: list) -> str:
        return ''.join(['\'', '\',\''.join(chain), '\''])


class EscapedOrChainer(ChainerInterface):
    def chain(self, chain: list) -> str:
        return '\\|'.join(chain)


def get_arg_filename() -> Optional[str]:
    filename = sys.argv[1:2]
    if not filename:
        return None

    return filename.pop()


def get_arg_title() -> str:
    title = sys.argv[2:3]
    if not title:
        return '[NO TITLE]'

    return title.pop()


def read_data(filename: Path) -> list:
    with filename.open('r') as file:
        data = []
        lines = file.readlines()

        for line in lines:
            line = line.strip(chr(10))
            line = line.strip(chr(13))
            data.append(line)

    return data


def get_chainers() -> List['ChainerInterface']:
    return [
        PlainChainer(),
        QuotedChainer(),
        EscapedOrChainer(),
    ]


def remove_duplicates(list_to_filter: list) -> list:
    return list(set(list_to_filter))


def display_block(block: str, title: str) -> None:
    print(title)
    print('-' * len(title))
    print(block)
    print('')


if __name__ == '__main__':
    filename = get_arg_filename()
    if not filename:
        print('No input file provided. Please enter a filename as a parameter. e.g.: chain source.txt')
        quit()

    filename = Path(filename)
    if not filename.is_file():
        print(f"The specified file ('{filename}') does not exist or the path is incorrect. Please check your input and try again.")
        quit()

    title = get_arg_title()
    data = remove_duplicates(read_data(filename))
    chainers = get_chainers()

    for chainer in chainers:
        block = chainer.chain(data)
        display_block(block, title)

    print(f"{len(data)} elements chained.")
