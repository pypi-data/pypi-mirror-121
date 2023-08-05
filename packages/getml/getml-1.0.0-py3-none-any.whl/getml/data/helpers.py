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
Collection of helper functions that are not intended to be used by
the end-user.
"""

import json
import numbers
import random
import string

import numpy as np
import pandas as pd  # type: ignore

import getml.communication as comm
from getml import constants, database
from getml.constants import COMPARISON_ONLY, TIME_STAMP
from getml.database import _retrieve_urls

from .columns import (
    BooleanColumnView,
    FloatColumn,
    FloatColumnView,
    StringColumn,
    StringColumnView,
    from_value,
)
from .roles import (
    _all_roles,
    _categorical_roles,
    _numerical_roles,
    time_stamp,
    unused_float,
    unused_string,
)
from .subroles import _all_subroles

# --------------------------------------------------------------------


def list_data_frames():
    """Lists all available data frames of the project.

        Examples:

            .. code-block:: python

                d, _ = getml.datasets.make_numerical()
                getml.data.list_data_frames()
                d.save()
                getml.data.list_data_frames()

    <<<<<<< HEAD
        Raises:
            IOError: If an error in the communication with the getML engine
            occurred.

    =======
    >>>>>>> develop
        Returns:
            dict:

                Dict containing lists of strings representing the names of
                the data frames objects

                * 'in_memory'
                    held in memory (RAM).
                * 'on_disk'
                    stored on disk.
    """

    cmd = dict()
    cmd["type_"] = "list_data_frames"
    cmd["name_"] = ""

    sock = comm.send_and_get_socket(cmd)

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    json_str = comm.recv_string(sock)

    sock.close()

    return json.loads(json_str)


# --------------------------------------------------------------------


def _check_if_exists(colnames, all_colnames):

    for col in colnames:
        if col in all_colnames:
            raise ValueError("Duplicate column: '" + col + "'!")

        all_colnames.append(col)

    return all_colnames


# --------------------------------------------------------------------


def _check_join_key(candidate, join_keys):
    if isinstance(candidate, str):
        candidate = [candidate]

    return [can for can in candidate if can not in join_keys]


# --------------------------------------------------------------------


def _empty_data_frame():
    return "Empty getml.DataFrame\nColumns: []\n"


# --------------------------------------------------------------------


def _exists_in_memory(name):

    if not isinstance(name, str):
        raise TypeError("'name' must be of type str")

    all_df = list_data_frames()

    return name in all_df["in_memory"]


# --------------------------------------------------------------------


def _extract_shape(cmd, name):
    shape = cmd[name + "_shape_"]
    shape = np.asarray(shape).astype(np.int32)
    return shape.tolist()


# --------------------------------------------------------------------


def _finditems(key, dct):
    if key in dct:
        yield dct[key]
    for k, v in dct.items():
        if isinstance(v, dict):
            yield from _finditems(key, v)


# --------------------------------------------------------------------


def _get_column(name, columns):
    for col in columns:
        if col.name == name:
            return col
    return None


# --------------------------------------------------------------------


def _handle_cols(cols):
    """
    Handles cols as supplied to DataFrame methods. Returns a list of column names.
    """

    if not isinstance(cols, list):
        cols = [cols]

    if not _is_typed_list(cols, (str, FloatColumn, StringColumn)):
        raise TypeError(
            "'cols' must be either a string, a FloatColumn, "
            "a StringColumn, or a list thereof."
        )

    names = []

    for col in cols:

        if isinstance(col, list):
            names.extend(_handle_cols(col))

        if isinstance(col, str):
            names.append(col)

        if isinstance(col, (FloatColumn, StringColumn)):
            names.append(col.name)

    return names


# --------------------------------------------------------------------


def _handle_multiple_join_keys(join_keys):
    on = [(jk, jk) if isinstance(jk, str) else jk for jk in join_keys]
    left_join_keys = [o[0] for o in on]
    right_join_keys = [o[1] for o in on]
    ljk, rjk = _merge_join_keys(left_join_keys, right_join_keys)
    return (ljk, rjk)


# --------------------------------------------------------------------


def _handle_on(on):
    if on is None:
        return (constants.NO_JOIN_KEY, constants.NO_JOIN_KEY)

    if isinstance(on, list):
        return _handle_multiple_join_keys(on)

    return on


# --------------------------------------------------------------------


def _handle_ts(ts):
    if ts is None:
        return ("", "")
    return ts


# --------------------------------------------------------------------


def _is_numerical_type(coltype):
    return coltype in [
        int,
        float,
        np.int_,
        np.int8,
        np.int16,
        np.int32,
        np.int64,
        np.uint8,
        np.uint16,
        np.uint32,
        np.uint64,
        np.float_,
        np.float16,
        np.float32,
        np.float64,
    ]


# --------------------------------------------------------------------


def _is_subclass_list(some_list, parent):

    is_subclass_list = isinstance(some_list, list)

    is_subclass_list = is_subclass_list and all(
        [issubclass(type(ll), parent) for ll in some_list]
    )

    return is_subclass_list


# --------------------------------------------------------------------


def _is_typed_dict(some_dict, key_types, value_types):

    if not isinstance(key_types, list):
        key_types = [key_types]

    if not isinstance(value_types, list):
        value_types = [value_types]

    is_typed_dict = isinstance(some_dict, dict)

    is_typed_dict = is_typed_dict and all(
        [any([isinstance(key, t) for t in key_types]) for key in some_dict.keys()]
    )

    is_typed_dict = is_typed_dict and all(
        [any([isinstance(val, t) for t in value_types]) for val in some_dict.values()]
    )

    return is_typed_dict


# --------------------------------------------------------------------


def _is_typed_list(some_list, types):

    if isinstance(types, list):
        types = tuple(types)

    is_typed_list = isinstance(some_list, list)

    is_typed_list = is_typed_list and all([isinstance(ll, types) for ll in some_list])

    return is_typed_list


# --------------------------------------------------------------------


def _is_non_empty_typed_list(some_list, types):
    return _is_typed_list(some_list, types) and len(some_list) > 0


# -----------------------------------------------------------------


def _make_id():
    letters = string.ascii_letters + string.digits
    return "".join([random.choice(letters) for _ in range(6)])


# --------------------------------------------------------------------


def _merge_join_keys(join_key, other_join_key):

    begin = constants.MULTIPLE_JOIN_KEYS_BEGIN
    end = constants.MULTIPLE_JOIN_KEYS_END
    sep = constants.JOIN_KEY_SEP
    len_jk = len_other_jk = 1

    if not other_join_key:
        other_join_key = join_key

    if _is_typed_list(join_key, str):
        len_jk = len(join_key)
        if len_jk > 1:
            join_key = begin + sep.join(join_key) + end
        else:
            join_key = join_key[0]

    if _is_typed_list(other_join_key, str):
        len_other_jk = len(other_join_key)
        if len_other_jk > 1:
            other_join_key = begin + sep.join(other_join_key) + end
        else:
            other_join_key = other_join_key[0]

    if len_jk != len_other_jk:
        raise ValueError(
            "The number of join keys passed to "
            + "'join_key' and 'other_join_key' "
            + "must match!"
        )

    return join_key, other_join_key


# --------------------------------------------------------------------


def _modify_pandas_columns(pandas_df):
    pandas_df_copy = pandas_df
    pandas_df_copy.columns = np.asarray(pandas_df.columns).astype(str).tolist()
    return pandas_df_copy


# --------------------------------------------------------------------


def _remove_trailing_underscores(some_dict):

    new_dict = dict()

    for kkey in some_dict:

        new_key = kkey

        if kkey[-1] == "_":
            new_key = kkey[:-1]

        if isinstance(some_dict[kkey], dict):
            new_dict[new_key] = _remove_trailing_underscores(some_dict[kkey])

        elif isinstance(some_dict[kkey], list):
            new_dict[new_key] = [
                _remove_trailing_underscores(elem) if isinstance(elem, dict) else elem
                for elem in some_dict[kkey]
            ]

        else:
            new_dict[new_key] = some_dict[kkey]

    return new_dict


# --------------------------------------------------------------------


def _update_sniffed_roles(sniffed_roles, roles):

    # -------------------------------------------------------

    if not isinstance(roles, dict):
        raise TypeError("roles must be a dict!")

    if not isinstance(sniffed_roles, dict):
        raise TypeError("sniffed_roles must be a dict!")

    for role in list(roles.keys()):
        if not _is_typed_list(roles[role], str):
            raise TypeError("Entries in roles must be lists of str!")

    for role in list(sniffed_roles.keys()):
        if not _is_typed_list(sniffed_roles[role], str):
            raise TypeError("Entries in sniffed_roles must be lists of str!")

    # -------------------------------------------------------

    for new_role in list(roles.keys()):

        for colname in roles[new_role]:

            for old_role in list(sniffed_roles.keys()):
                if colname in sniffed_roles[old_role]:
                    sniffed_roles[old_role].remove(colname)
                    break

            if new_role in sniffed_roles:
                sniffed_roles[new_role] += [colname]
            else:
                sniffed_roles[new_role] = [colname]

    # -------------------------------------------------------

    return sniffed_roles


# ------------------------------------------------------------


def _send_numpy_array(col, numpy_array, sock=None):

    # -------------------------------------------

    if sock is None:
        sock = comm.send_and_get_socket(col.cmd)
    else:
        cmd = json.dumps(col.cmd)
        comm.send_string(sock, cmd)

    # -------------------------------------------

    if col.cmd["type_"] == "StringColumn":
        if pd.api.types.is_datetime64_dtype(numpy_array):
            str_array = np.datetime_as_string(numpy_array, unit="us")
        else:
            str_array = numpy_array.astype(str)

        comm.send_string_column(sock, str_array)

    elif col.cmd["type_"] == "FloatColumn":
        comm.send_float_matrix(sock, numpy_array)

    # -------------------------------------------

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)


# --------------------------------------------------------------------


def _sniff_csv(
    fnames, num_lines_sniffed=1000, quotechar='"', sep=",", skip=0, colnames=None
):
    """Sniffs a list of CSV files and returns the result as a dictionary of
    roles.

    Args:
        fnames (List[str]): The list of CSV file names to be read.

        num_lines_sniffed (int, optional):

            Number of lines analysed by the sniffer.

        quotechar (str, optional):

            The character used to wrap strings.

        sep (str, optional):

            The character used for separating fields.

        skip (int, optional):
            Number of lines to skip at the beginning of each file.

        colnames(List[str] or None, optional): The first line of a CSV file
            usually contains the column names. When this is not the case, you need to
            explicitly pass them.

    Returns:
        dict: Keyword arguments (kwargs) that can be used to construct
              a DataFrame.
    """
    # ----------------------------------------------------------------

    fnames_ = _retrieve_urls(fnames, verbose=False)

    # ----------------------------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = ""
    cmd["type_"] = "Database.sniff_csv"

    cmd["dialect_"] = "python"
    cmd["fnames_"] = fnames_
    cmd["num_lines_sniffed_"] = num_lines_sniffed
    cmd["quotechar_"] = quotechar
    cmd["sep_"] = sep
    cmd["skip_"] = skip
    cmd["conn_id_"] = "default"

    if colnames is not None:
        cmd["colnames_"] = colnames

    # ----------------------------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_get_socket(cmd)

    # ----------------------------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    if msg != "Success!":
        sock.close()
        raise IOError(msg)

    # ----------------------------------------------------------------

    roles = comm.recv_string(sock)

    sock.close()

    return json.loads(roles)


# --------------------------------------------------------------------


def _sniff_db(table_name, conn=None):
    """
    Sniffs a table in the database and returns a dictionary of roles.

    Args:
        table_name (str): Name of the table to be sniffed.

        conn (:class:`~getml.database.Connection`, optional): The database
            connection to be used. If you don't explicitly pass a connection,
            the engine will use the default connection.

    Returns:
        dict: Keyword arguments (kwargs) that can be used to construct
              a DataFrame.
    """

    # -------------------------------------------

    conn = conn or database.Connection()

    # ----------------------------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = table_name
    cmd["type_"] = "Database.sniff_table"

    cmd["conn_id_"] = conn.conn_id

    # ----------------------------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_get_socket(cmd)

    # ----------------------------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    if msg != "Success!":
        sock.close()
        raise Exception(msg)

    # ----------------------------------------------------------------

    roles = comm.recv_string(sock)

    sock.close()

    return json.loads(roles)


# --------------------------------------------------------------------


def _sniff_json(json_str):
    """Sniffs a JSON str and returns the result as a dictionary of
    roles.

    Args:
        json_str (str): The JSON string to be sniffed.

    Returns:
        dict: Roles that can be used to construct a DataFrame.
    """
    json_dict = json.loads(json_str)

    roles = dict()
    roles["unused_float"] = []
    roles["unused_string"] = []

    for cname, col in json_dict.items():
        if _is_numerical_type(np.array(col).dtype):
            roles["unused_float"].append(cname)
        else:
            roles["unused_string"].append(cname)

    return roles


# --------------------------------------------------------------------


def _sniff_pandas(pandas_df):
    """Sniffs a pandas.DataFrame and returns the result as a dictionary of
    roles.

    Args:
        pandas_df (pandas.DataFrame): The pandas.DataFrame to be sniffed.

    Returns:
        dict: Roles that can be used to construct a DataFrame.
    """
    roles = dict()
    roles["unused_float"] = []
    roles["unused_string"] = []

    colnames = pandas_df.columns
    coltypes = pandas_df.dtypes

    for cname, ctype in zip(colnames, coltypes):
        if _is_numerical_type(ctype):
            roles["unused_float"].append(cname)
        else:
            roles["unused_string"].append(cname)

    return roles


# --------------------------------------------------------------------


def _sniff_s3(
    bucket, keys, region, num_lines_sniffed=1000, sep=",", skip=0, colnames=None
):
    """Sniffs a list of CSV files located in an S3 bucket
        and returns the result as a dictionary of roles.

        Args:
            bucket (str):
                The bucket from which to read the files.

            keys (List[str]): The list of keys (files in the bucket) to be read.

            region (str):
                The region in which the bucket is located.

            num_lines_sniffed (int, optional):
                Number of lines analysed by the sniffer.

            sep (str, optional):
                The character used for separating fields.

            skip (int, optional):
                Number of lines to skip at the beginning of each file.

            colnames(List[str] or None, optional): The first line of a CSV file
                usually contains the column names. When this is not the case, you need to
                explicitly pass them.
    <<<<<<< HEAD
        Raises:
            IOError: If an error in the communication with the getML engine
            occurred.
    =======
    >>>>>>> develop

        Returns:
            dict: Keyword arguments (kwargs) that can be used to construct
                  a DataFrame.
    """

    # ----------------------------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = ""
    cmd["type_"] = "Database.sniff_s3"

    cmd["bucket_"] = bucket
    cmd["dialect_"] = "python"
    cmd["keys_"] = keys
    cmd["num_lines_sniffed_"] = num_lines_sniffed
    cmd["region_"] = region
    cmd["sep_"] = sep
    cmd["skip_"] = skip
    cmd["conn_id_"] = "default"

    if colnames is not None:
        cmd["colnames_"] = colnames

    # ----------------------------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_get_socket(cmd)

    # ----------------------------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    if msg != "Success!":
        sock.close()
        raise IOError(msg)

    # ----------------------------------------------------------------

    roles = comm.recv_string(sock)

    sock.close()

    return json.loads(roles)


# --------------------------------------------------------------------


def _check_role(role):

    correct_role = isinstance(role, str)
    correct_role = correct_role and role in _all_roles

    if not correct_role:
        raise ValueError(
            """'role' must be None or of type str and in """ + str(_all_roles) + "."
        )


# ------------------------------------------------------------


def _transform_col(col, role, is_boolean, is_float, is_string, time_formats):

    if (is_boolean or is_float) and role in _categorical_roles:
        return col.as_str()  # pytype: disable=attribute-error

    if (is_boolean or is_string) and role in _numerical_roles:
        if role == time_stamp:
            return col.as_ts(  # pytype: disable=attribute-error
                time_formats=time_formats
            )

        return col.as_num()  # pytype: disable=attribute-error

    return col


# --------------------------------------------------------------------


def _transform_timestamps(time_stamps):
    """Transforming a time stamp using to_numeric
    will result in the number of nanoseconds since
    the beginning of UNIX time. We want the number of seconds since
    UNIX time."""

    if not isinstance(time_stamps, pd.DataFrame):
        raise TypeError("'time_stamps' must be a pandas.DataFrame!")

    transformed = pd.DataFrame()

    for colname in time_stamps.columns:

        if pd.api.types.is_numeric_dtype(time_stamps[colname]):
            transformed[colname] = time_stamps[colname]

        elif pd.api.types.is_datetime64_ns_dtype(time_stamps[colname]):
            transformed[colname] = (
                time_stamps[[colname]]
                .apply(pd.to_datetime, errors="coerce")
                .apply(pd.to_numeric, errors="coerce")
                .apply(lambda val: val / 1.0e9)[colname]
            )

        else:
            raise TypeError(
                """
                Column '"""
                + colname
                + """' has the wrong type!

                If you want to send a numpy array or a column in a
                pandas.DataFrame to the engine as a time_stamp, its
                type must either be numerical or numpy.datetime64.

                To fix this problem, you can do one of the following:
                1) Read it in as an unused_string and then use
                   set_role(...) to make it a time stamp. (You might
                   have to explicitly set time_formats.)

                2) Cast your column or array as a numerical value
                   or a numpy.datetime64."""
            )

    return transformed.values


# --------------------------------------------------------------------


def _with_column(col, name, role=None, subroles=None, unit="", time_formats=None):

    # ------------------------------------------------------------

    if isinstance(col, (bool, str, numbers.Number, np.datetime64)):
        col = from_value(col)

    # ------------------------------------------------------------

    if not isinstance(
        col,
        (
            FloatColumn,
            FloatColumnView,
            StringColumn,
            StringColumnView,
            BooleanColumnView,
        ),
    ):
        raise TypeError("'col' must be a getml.data.Column or a value!")

    # ------------------------------------------------------------

    is_boolean = col.cmd["type_"] == "BooleanColumnView"

    if not is_boolean:
        subroles = subroles or col.subroles  # pytype: disable=attribute-error
        unit = unit or col.unit  # pytype: disable=attribute-error

    # ------------------------------------------------------------

    subroles = subroles or []

    if isinstance(subroles, str):
        subroles = [subroles]

    # ------------------------------------------------------------

    if not isinstance(name, str):
        raise TypeError("'name' must be of type str")

    if not _is_typed_list(subroles, str):
        raise TypeError("'subroles' must be of type str, List[str] or None.")

    if not isinstance(unit, str):
        raise TypeError("'unit' must be of type str")

    # ------------------------------------------------------------

    invalid_subroles = [r for r in subroles if r not in _all_subroles]

    if invalid_subroles:
        raise ValueError(
            "'subroles' must be from getml.data.subroles, "
            + "meaning it is one of the following: "
            + str(_all_subroles)
            + ", got "
            + str(invalid_subroles)
        )

    # ------------------------------------------------------------

    time_formats = time_formats or constants.TIME_FORMATS

    # ------------------------------------------------------------

    is_string = "StringColumn" in col.cmd["type_"]

    is_float = "FloatColumn" in col.cmd["type_"]

    # ------------------------------------------------------------

    correct_coltype = is_boolean or is_string or is_float

    if not correct_coltype:
        raise TypeError("""'col' must be a getml.data.Column.""")

    # ------------------------------------------------------------

    if role is None:
        role = unused_float if is_float else unused_string

    _check_role(role)

    # ------------------------------------------------------------

    return (
        _transform_col(col, role, is_boolean, is_float, is_string, time_formats),
        role,
        subroles,
    )


# --------------------------------------------------------------------


def _with_role(base, cols, role, time_formats):

    # ------------------------------------------------------------

    time_formats = time_formats or constants.TIME_FORMATS

    # ------------------------------------------------------------

    names = _handle_cols(cols)

    if not isinstance(role, str):
        raise TypeError("'role' must be str.")

    if not _is_non_empty_typed_list(time_formats, str):
        raise TypeError("'time_formats' must be a non-empty list of str")

    # ------------------------------------------------------------

    for nname in names:
        if nname not in base.colnames:
            raise ValueError("No column called '" + nname + "' found.")

    if role not in _all_roles:
        raise ValueError(
            "'role' must be one of the following values: " + str(_all_roles)
        )

    # ------------------------------------------------------------

    view = base

    for name in names:
        col = view[name]
        unit = TIME_STAMP + COMPARISON_ONLY if role == time_stamp else col.unit
        view = view.with_column(
            col=col,
            name=name,
            role=role,
            subroles=col.subroles,
            unit=unit,
            time_formats=time_formats,
        )

    # ------------------------------------------------------------

    return view


# ------------------------------------------------------------


def _with_subroles(base, cols, subroles, append=False):

    names = _handle_cols(cols)

    if isinstance(subroles, str):
        subroles = [subroles]

    if not _is_non_empty_typed_list(names, str):
        raise TypeError("'names' must be either a string or a list of strings.")

    if not _is_typed_list(subroles, str):
        raise TypeError("'subroles' must be either a string or a list of strings.")

    if not isinstance(append, bool):
        raise TypeError("'append' must be a bool.")

    # ------------------------------------------------------------

    if [r for r in subroles if r not in _all_subroles]:
        raise ValueError(
            "'subroles' must be from getml.data.subroles, "
            + "meaning it is one of the following: "
            + str(_all_subroles)
        )

    # ------------------------------------------------------------

    view = base

    for name in names:
        col = view[name]
        view = view.with_column(
            col=col,
            name=name,
            role=view.roles.infer(name),
            subroles=subroles,
            unit=col.unit,
            time_formats=None,
        )

    # ------------------------------------------------------------

    return view


# ------------------------------------------------------------


def _with_unit(base, cols, unit, comparison_only=False):

    names = _handle_cols(cols)

    if not isinstance(unit, str):
        raise TypeError("Parameter 'unit' must be a str.")

    # ------------------------------------------------------------

    if comparison_only:
        unit += constants.COMPARISON_ONLY

    # ------------------------------------------------------------

    view = base

    for name in names:
        col = view[name]
        view = view.with_column(
            col=col,
            name=name,
            role=view.roles.infer(name),
            subroles=col.subroles,
            unit=unit,
            time_formats=None,
        )

    # ------------------------------------------------------------

    return view


# --------------------------------------------------------------------
