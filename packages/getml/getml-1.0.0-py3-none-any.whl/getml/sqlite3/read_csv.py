# Copyright 2021 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
Contains utility functions for reading CSV files
into sqlite3.
"""

import csv
import sqlite3

from getml.data.helpers import _is_typed_list, _is_non_empty_typed_list

from .helpers import _create_table, _log
from .read_list import read_list
from .sniff_csv import sniff_csv

# ----------------------------------------------------------------------------


def _read_csv_file(fname, sep, quotechar, header, skip=0):
    with open(fname, newline="\n") as csvfile:
        reader = csv.reader(csvfile, delimiter=sep, quotechar=quotechar)
        if header:
            return list(reader)[skip + 1 :]
        return list(reader)[skip:]


# ----------------------------------------------------------------------------


def read_csv(
    conn,
    fnames,
    table_name,
    header=True,
    if_exists="append",
    quotechar='"',
    sep=",",
    skip=0,
    colnames=None,
):
    """
    Reads a list of CSV files and writes them into an sqlite3 table.

    Args:
        conn (sqlite3.Connection):
            A sqlite3 connection created by :func:`~getml.sqlite3.connect`.

        fnames (str or List[str]):
            The names of the CSV files.

        fnames (str or List[str]):
            The names of the CSV files.

        table_name (str):
            The name of the table to write to.

        header (bool):
            Whether the csv file contains a header. If True, the first line
            is skipped and column names are inferred accordingly.

        quotechar (str):
            The string escape character.

        if_exists (str):
            How to behave if the table already exists:

                - 'fail': Raise a ValueError.
                - 'replace': Drop the table before inserting new values.
                - 'append': Insert new values to the existing table.

        sep (str):
            The field separator.

        skip (int):
            The number of lines to skip (before a possible header)

        colnames(List[str] or None, optional):
            The first line of a CSV file
            usually contains the column names. When this is not the case, you can
            explicitly pass them. If you pass colnames, it is assumed that the
            CSV files do not contain a header, thus overriding the 'header' variable.
    """
    # ------------------------------------------------------------

    if not isinstance(fnames, list):
        fnames = [fnames]

    # ------------------------------------------------------------

    if not isinstance(conn, sqlite3.Connection):
        raise TypeError("'conn' must be an sqlite3.Connection object")

    if not _is_non_empty_typed_list(fnames, str):
        raise TypeError("'fnames' must be a string or a non-empty list of strings")

    if not isinstance(table_name, str):
        raise TypeError("'table_name' must be a string")

    if not isinstance(header, bool):
        raise TypeError("'header' must be a bool")

    if not isinstance(quotechar, str):
        raise TypeError("'quotechar' must be a str")

    if not isinstance(if_exists, str):
        raise TypeError("'if_exists' must be a str")

    if not isinstance(sep, str):
        raise TypeError("'sep' must be a str")

    if not isinstance(skip, int):
        raise TypeError("'skip' must be an int")

    if colnames is not None and not _is_typed_list(colnames, str):
        raise TypeError("'colnames' must be a list of strings or None")

    # ------------------------------------------------------------

    schema = sniff_csv(
        fnames=fnames,
        table_name=table_name,
        header=header,
        quotechar=quotechar,
        sep=sep,
        skip=skip,
        colnames=colnames,
    )

    _create_table(conn, table_name, schema, if_exists)

    for fname in fnames:
        _log("Loading '" + fname + "' into '" + table_name + "'...")
        data = _read_csv_file(fname, sep, quotechar, header and not colnames, skip)
        read_list(conn, table_name, data)
