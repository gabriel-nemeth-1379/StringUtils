#!/usr/bin/env python3

from pathlib import Path
from typing import List
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


class ArgsReader:
    def get_arg_filename(self) -> str:
        filename = sys.argv[1:2]
        if not filename:
            return ''

        return filename.pop()

    def get_arg_title(self) -> str:
        title = sys.argv[2:3]
        if not title:
            return '[NO TITLE]'

        return title.pop()


class FileReader:
    def read_data(self, filename: str) -> list:
        filename = Path(filename)
        if not filename.is_file():
            raise FileNotFoundError

        with filename.open('r') as file:
            data = []
            lines = file.readlines()

            for line in lines:
                line = line.strip(chr(10))
                line = line.strip(chr(13))
                data.append(line)

        return data


class App:
    def __init__(self):
        self._args_reader = ArgsReader()
        self._file_reader = FileReader()

    def run(self):
        data = self._read_data()
        data = self._remove_duplicates(data)

        title = self._args_reader.get_arg_title()
        chainers = self._get_chainers()
        for chainer in chainers:
            block = chainer.chain(data)
            self._display_block(block, title)

        print(f"{len(data)} elements chained.")

    def _read_data(self) -> list:
        filename = self._args_reader.get_arg_filename()
        if not filename:
            print('No input file provided. Please enter a filename as a parameter. e.g.: chain source.txt')
            quit()

        data = []
        try:
            data = self._file_reader.read_data(filename)
        except FileNotFoundError:
            print(f"The specified file ('{filename}') does not exist or the path is incorrect.\n"
                  "Please check your input and try again.")
            quit()

        return data

    def _get_chainers(self) -> List['ChainerInterface']:
        return [
            PlainChainer(),
            QuotedChainer(),
            EscapedOrChainer(),
        ]

    def _remove_duplicates(self, list_to_filter: list) -> list:
        return list(set(list_to_filter))

    def _display_block(self, block: str, title: str) -> None:
        display_format = f"{title}\n"\
                         f"{'-' * len(title)}\n"\
                         f"{block}\n"

        print(display_format)


if __name__ == '__main__':
    app = App()
    app.run()
