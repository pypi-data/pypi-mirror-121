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
Handles the communication for the getML library
"""

import json
import numbers
import pathlib
import socket
import sys

import numpy as np

from .version import __version__

# --------------------------------------------------------------------

port = 1708
"""
The port of the getML engine. The port is automaticallly set
according to the process spawned when setting a project.
The monitor automatically looks up a free port (starting from 1708).
Setting the port here has no effect.
"""

tcp_port = 1711
"""
The TCP port of the getML monitor.
"""

# --------------------------------------------------------------------

ENGINE_CANNOT_CONNECT_ERROR_MSG = (
    """Cannot reach the getML engine. Please make sure you have set a project."""
)

MONITOR_CANNOT_CONNECT_ERROR_MSG = (
    """Cannot reach the getML monitor. Please make sure the getML app is running."""
)

GETML_SEP = "$GETML_SEP"

SEP_SIZE = np.uint64(10)

# --------------------------------------------------------------------


def is_monitor_alive():
    """Checks if the getML monitor is running.

    Returns:
        bool:
            True if the getML monitor is running and ready to accept
            commands and False otherwise.
    """

    # ---------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("localhost", tcp_port))
    except ConnectionRefusedError:
        return False

    sock.close()

    return True


# --------------------------------------------------------------------


class _GetmlEncoder(json.JSONEncoder):
    """Enables a custom serialization of the getML classes."""

    def default(self, obj):
        """Checks for the particular type of the provided object and
        deserializes it into an escaped string.

        To ensure the getML can handle all keys, we have to add a
        trailing underscore.

        Args:
            obj: Any of the classes defined in the getml package.

        Returns:
            string:
                Encoded JSON.

        Examples:
            Create a :class:`~getml.predictors.LinearRegression`,
            serialize it, and deserialize it again.

            .. code-block:: python

                p = getml.predictors.LinearRegression()
                p_serialized = json.dumps(
                    p, cls = getml.communication._GetmlEncoder)
                p2 = json.loads(
                    p_serialized,
                    object_hook=getml.helpers.predictors._decode_predictor
                )
                p == p2

        """

        if hasattr(obj, "_getml_deserialize"):
            return obj._getml_deserialize()

        return json.JSONEncoder.default(self, obj)


# --------------------------------------------------------------------


class _ProgressBar:
    """Displays progress in bar form."""

    def __init__(self):
        self.length = 40

    def show(self, progress):
        """Displays an updated version of the progress bar.

        Args:
            progress (float): The progress to be shown. Must
                be between 0 and 100.
        """
        done = int(progress * self.length / 100.0)

        remaining = self.length - done

        pbar = "[" + "=" * done
        pbar += " " * remaining + "] "
        pbar += str(progress) + "%"

        end = "\r"

        print(pbar, end=end, flush=True)


# --------------------------------------------------------------------


def _make_error_msg():
    if not is_monitor_alive():
        return MONITOR_CANNOT_CONNECT_ERROR_MSG
    else:
        msg = ENGINE_CANNOT_CONNECT_ERROR_MSG
        msg += "\n\nTo set: `getml.engine.set_project`"
        return msg


# --------------------------------------------------------------------


def engine_exception_handler(msg, fallback=""):
    """Looks at the error message thrown by the engine and decides whether
    to throw a corresponding Exception using the same string or
    altering the message first.

    In either way, this function will always throw some sort of Exception.

    Args:

        msg (str): Error message returned by the getML engine.
        fallback (str):

            If not empty, the default Exception will carry this
            string.
    """

    if not fallback:
        fallback = msg

    raise IOError(fallback)


# --------------------------------------------------------------------


def recv_data(sock, size):
    """Receives data (of any type) sent by the getml engine."""

    # ----------------------------------------------------------------

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    if not isinstance(size, numbers.Real):
        raise TypeError("'size' must be a number.")

    # ----------------------------------------------------------------

    data = []

    bytes_received = np.uint64(0)

    max_chunk_size = np.uint64(2048)

    while bytes_received < size:

        current_chunk_size = int(min(size - bytes_received, max_chunk_size))

        chunk = sock.recv(current_chunk_size)

        if not chunk:
            raise IOError(
                """The getML engine died unexpectedly.
                    If this wasn't done on purpose, please get in contact
                    with our support or file a bug report."""
            )

        data.append(chunk)

        bytes_received += np.uint64(len(chunk))

    return "".encode().join(data)


# --------------------------------------------------------------------


def recv_boolean_column(sock):
    """Receives a column (type boolean) from the getml engine."""

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    # ----------------------------------------------------------------

    # By default, numeric data sent over the socket is big endian,
    # also referred to as network-byte-order!
    if sys.byteorder == "little":
        shape_str = recv_data(sock, np.nbytes[np.int32] * 2)

        shape = np.frombuffer(shape_str, dtype=np.int32).byteswap().astype(np.uint64)

        size = shape[0] * shape[1] * np.uint64(np.nbytes[np.int32])

        matrix = recv_data(sock, size)

        matrix = np.frombuffer(matrix, dtype=np.int32).byteswap()

        matrix = matrix.reshape(shape[0], shape[1])

    else:
        shape_str = recv_data(sock, np.nbytes[np.int32] * 2)

        shape = np.frombuffer(shape_str, dtype=np.int32).astype(np.uint64)

        size = shape[0] * shape[1] * np.uint64(np.nbytes[np.int32])

        matrix = recv_data(sock, size)

        matrix = np.frombuffer(matrix, dtype=np.int32)

        matrix = matrix.reshape(shape[0], shape[1])

    return matrix == 1


# --------------------------------------------------------------------


def recv_float_matrix(sock):
    """
    Receives a matrix (type np.float64) from the getml engine.
    """

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    # ----------------------------------------------------------------

    # By default, numeric data sent over the socket is big endian,
    # also referred to as network-byte-order!
    if sys.byteorder == "little":
        shape_str = recv_data(sock, np.nbytes[np.int32] * 2)

        shape = np.frombuffer(shape_str, dtype=np.int32).byteswap().astype(np.uint64)

        size = shape[0] * shape[1] * np.uint64(np.nbytes[np.float64])

        matrix = recv_data(sock, size)

        matrix = np.frombuffer(matrix, dtype=np.float64).byteswap()

        matrix = matrix.reshape(shape[0], shape[1])

    else:
        shape_str = recv_data(sock, np.nbytes[np.int32] * 2)

        shape = np.frombuffer(shape_str, dtype=np.int32).astype(np.uint64)

        size = shape[0] * shape[1] * np.uint64(np.nbytes[np.float64])

        matrix = recv_data(sock, size)

        matrix = np.frombuffer(matrix, dtype=np.float64)

        matrix = matrix.reshape(shape[0], shape[1])

    return matrix


# --------------------------------------------------------------------


def recv_string(sock):
    """
    Receives a string from the getml engine
    (an actual string, not a bytestring).
    """

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    # ----------------------------------------------------------------

    # By default, numeric data sent over the socket is big endian,
    # also referred to as network-byte-order!
    if sys.byteorder == "little":

        size_str = recv_data(sock, np.nbytes[np.int32])

        size = np.frombuffer(size_str, dtype=np.int32).byteswap()[0]

    else:
        size_str = recv_data(sock, np.nbytes[np.int32])

        size = np.frombuffer(size_str, dtype=np.int32)[0]

    data = recv_data(sock, size)

    return data.decode(errors="ignore")


# --------------------------------------------------------------------


def recv_string_column(sock):
    """
    Receives a column of type string from the getml engine
    """

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    # ----------------------------------------------------------------

    nbytes_str = recv_data(sock, np.nbytes[np.uint64])

    if sys.byteorder == "little":
        nbytes = np.frombuffer(nbytes_str, dtype=np.uint64).byteswap()[0]
    else:
        nbytes = np.frombuffer(nbytes_str, dtype=np.uint64)[0]

    # ----------------------------------------------------------------

    col = (
        recv_data(sock, nbytes).decode(errors="ignore").split(GETML_SEP)
        if nbytes != 0
        else []
    )

    # ----------------------------------------------------------------

    col = np.asarray(col, dtype=object)

    return col.reshape(len(col), 1)


# --------------------------------------------------------------------


def recv_warnings(sock):
    """
    Receives a set of warnings to raise from the getml engine.
    """

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    json_str = recv_string(sock)

    if json_str[0] != "{":
        raise ValueError(json_str)

    json_obj = json.loads(json_str)

    all_warnings = json_obj["warnings_"]

    for warning in all_warnings:
        print(warning)

    return len(all_warnings) == 0


# --------------------------------------------------------------------


def send(cmd):
    """Sends a command to the getml engine and closes the established
    connection.

    Creates a socket and sends a command to the getML engine using the
    module-wide variable :py:const:`~getml.port`.

    A message (string) from the :py:class:`socket.socket` will be
    received using :py:func:`~getml.recv_string` and the socket will
    be closed. If the message is "Success!", everything work
    properly. Else, an Exception will be thrown containing the
    message.

    In case another message is supposed to be send by the engine,
    :py:func:`~getml.communication.send_and_get_socket` has to be used
    and the calling function must handle the message itself!

    Please be very careful when altering the routing/calling behavior
    of the socket communication! The engine might react in a quite
    sensible and freezing way.

    Arg:
        cmd (dict): A dictionary specifying the command the engine is
            supposed to execute. It _must_ contain at least two string
            values with the corresponding keys being named "name_" and
            "type_".
    """

    if not isinstance(cmd, dict):
        raise TypeError("'cmd' must be a dict.")

    # ----------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(("localhost", port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(_make_error_msg())

    # Use a custom encoder which knows how to handle the classes
    # defined in the getml package.
    msg = json.dumps(cmd, cls=_GetmlEncoder)

    send_string(sock, msg)

    # ---------------------------------------------------------------
    # The calling function does not want to further use the
    # socket. Therefore, it will be checked here whether the
    # request was successful and closed.
    msg = recv_string(sock)

    sock.close()

    if msg != "Success!":
        engine_exception_handler(msg)


# --------------------------------------------------------------------


def send_and_get_socket(cmd):
    """Sends a command to the getml engine and returns the established
    connection.

    Creates a socket and sends a command to the getML engine using the
    module-wide variable :py:const:`~getml.port`.

    The function will return the socket it opened and the calling
    function is free to receive whatever data is desires over it. But
    the latter has also to take care of closing the socket afterwards
    itself!

    Please be very careful when altering the routing/calling behavior
    of the socket communication! The engine might react in a quite
    sensible and freezing way. Especially implemented handling of
    socket sessions (their passing from function to function) must not
    be altered or separated in distinct calls to the
    :py:func:`~getml.communication.send` function! Some commands have
    to be send via the same socket or the engine will not be able to
    handle them and might block.

    Arg:
        cmd (dict): A dictionary specifying the command the engine is
            supposed to execute. It _must_ contain at least two string
            values with the corresponding keys being named "name_" and
            "type_"."

    Returns:
        :py:class:`socket.socket`: A socket using which the Python API
            can communicate with the getML engine.
    """

    if not isinstance(cmd, dict):
        raise TypeError("'cmd' must be a dict.")

    # ----------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(("localhost", port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(_make_error_msg())

    # Use a custom encoder which knows how to handle the classes
    # defined in the getml package.
    msg = json.dumps(cmd, cls=_GetmlEncoder)

    send_string(sock, msg)

    # ----------------------------------------------------------------

    return sock


# --------------------------------------------------------------------


def send_string_column(sock, string_column):
    """Sends a list of strings to the getml engine
    (an actual string, not a bytestring).
    """

    # ----------------------------------------------------------------

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    if not isinstance(string_column, np.ndarray):
        raise TypeError("'string_column' must be a numpy.ndarray.")

    if len(string_column.shape) > 2 or len(string_column.shape) == 0:
        raise Exception("Numpy array must be one-dimensional or two-dimensional!")

    if len(string_column.shape) == 2 and string_column.shape[1] != 1:
        raise Exception("Numpy array must be single column!")

    # ----------------------------------------------------------------

    def get_len(string):
        return np.uint64(len(string.encode("utf-8")))

    # ----------------------------------------------------------------

    def calc_nbytes(flattened):
        if len(flattened) == 0:
            return np.uint64(0)
        nbytes_data = np.uint64(sum(get_len(string) for string in flattened))
        nbytes_sep = np.uint64(len(flattened) - 1) * SEP_SIZE
        return nbytes_data + nbytes_sep

    # ----------------------------------------------------------------

    flattened = string_column.flatten()

    nbytes = calc_nbytes(flattened)

    # ----------------------------------------------------------------

    # By default, numeric data sent over the socket is big endian,
    # also referred to as network-byte-order!
    if sys.byteorder == "little":
        sock.sendall(np.asarray([nbytes]).astype(np.uint64).byteswap().tobytes())
    else:
        sock.sendall(np.asarray([nbytes]).astype(np.uint64).tobytes())

    # ----------------------------------------------------------------

    sock.sendall(GETML_SEP.join(flattened).encode("utf-8"))


# --------------------------------------------------------------------


def send_float_matrix(sock, matrix):
    """Sends a matrix (type np.float64) to the getml engine."""

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    if not isinstance(matrix, np.ndarray):
        raise TypeError("'matrix' must be a numpy.ndarray.")

    # ----------------------------------------------------------------

    if len(matrix.shape) == 1:
        shape = [matrix.shape[0], 1]

    elif len(matrix.shape) > 2:
        raise Exception("Numpy array must be one-dimensional or two-dimensional!")

    else:
        shape = matrix.shape

    # By default, numeric data sent over the socket is big endian,
    # also referred to as network-byte-order!
    if sys.byteorder == "little":

        sock.sendall(np.asarray(shape).astype(np.int32).byteswap().tobytes())

        sock.sendall(matrix.astype(np.float64).byteswap().tobytes())

    else:

        sock.sendall(np.asarray(shape).astype(np.int32).tobytes())

        sock.sendall(matrix.astype(np.float64).tobytes())


# --------------------------------------------------------------------


def send_string(sock, string):
    """
    Sends a string to the getml engine
    (an actual string, not a bytestring).
    """

    if not isinstance(sock, socket.socket):
        raise TypeError("'sock' must be a socket.")

    if not isinstance(string, str):
        raise TypeError("'string' must be a str.")

    # ----------------------------------------------------------------

    encoded = string.encode("utf-8")

    size = len(encoded)

    # By default, numeric data sent over the socket is big endian,
    # also referred to as network-byte-order!
    if sys.byteorder == "little":

        sock.sendall(np.asarray([size]).astype(np.int32).byteswap().tobytes())

    else:

        sock.sendall(np.asarray([size]).astype(np.int32).tobytes())

    sock.sendall(encoded)


# --------------------------------------------------------------------


def log(sock):
    """
    Prints all the logs received by the socket.
    """
    pbar = _ProgressBar()

    while True:
        msg = recv_string(sock)

        if msg[:5] != "log: ":
            print()
            print()
            return msg

        msg = msg[5:]

        if "Progress: " in msg:
            msg = msg.split("Progress: ")[1].split("%")[0]
            progress = int(msg)
            pbar.show(progress)
            continue

        print()
        print()
        print(msg)
        pbar.show(0)


# --------------------------------------------------------------------


def _delete_project(name):

    # ----------------------------------------------------------------

    if not isinstance(name, str):
        raise TypeError("'name' must be of type str")

    # ----------------------------------------------------------------

    if name in _list_projects_impl(running_only=True):
        _suspend_project(name)

    # ----------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "deleteproject"
    cmd["body_"] = name

    # ----------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("localhost", tcp_port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(_make_error_msg())

    msg = json.dumps(cmd, cls=_GetmlEncoder)

    send_string(sock, msg)

    # ----------------------------------------------------------------

    msg = recv_string(sock)

    if msg != "Success!":
        engine_exception_handler(msg)

    # ----------------------------------------------------------------

    sock.close()


# --------------------------------------------------------------------


def _get_project_name():
    cmd = dict()
    cmd["type_"] = "project_name"
    cmd["name_"] = ""

    sock = send_and_get_socket(cmd)

    pname = recv_string(sock)

    sock.close()

    return pname


# --------------------------------------------------------------------


def _load_project(bundle, name=None):

    name = name or ""

    # ----------------------------------------------------------------

    if not isinstance(name, str):
        raise TypeError("'name' must be of type str")

    # ----------------------------------------------------------------

    bundle = pathlib.Path(bundle).resolve().as_posix()

    cmd = dict()
    cmd["type_"] = "loadproject"
    cmd["body_"] = dict(bundle_=bundle, name_=name)

    # ----------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("localhost", tcp_port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(_make_error_msg())

    msg = json.dumps(cmd, cls=_GetmlEncoder)

    send_string(sock, msg)

    # ----------------------------------------------------------------

    msg = log(sock)

    if msg != "Success!":
        engine_exception_handler(msg)

    global port
    port = int(recv_string(sock))

    proj_name = _get_project_name()

    # ----------------------------------------------------------------

    print()
    print(f"Loaded {bundle}\n as {proj_name}. Connected to {proj_name}.")


# --------------------------------------------------------------------


def _list_projects_impl(running_only):

    # ----------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "listallprojects"
    cmd["body_"] = ""

    # ----------------------------------------------------------------

    if running_only:
        cmd["type_"] = "listrunningprojects"

    # ----------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("localhost", tcp_port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(_make_error_msg())

    msg = json.dumps(cmd, cls=_GetmlEncoder)

    send_string(sock, msg)

    # ----------------------------------------------------------------

    msg = recv_string(sock)

    if msg != "Success!":
        engine_exception_handler(msg)

    # ----------------------------------------------------------------

    json_str = recv_string(sock)

    sock.close()

    # ----------------------------------------------------------------

    return json.loads(json_str)["projects"]


# --------------------------------------------------------------------


def _monitor_url():

    cmd = dict()

    cmd["type_"] = "monitor_url"
    cmd["name_"] = ""

    sock = send_and_get_socket(cmd)

    return recv_string(sock)


# --------------------------------------------------------------------


def _check_version():

    cmd = dict()
    cmd["type_"] = "getversion"
    cmd["body_"] = ""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("localhost", tcp_port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(_make_error_msg())

    msg = json.dumps(cmd, cls=_GetmlEncoder)

    send_string(sock, msg)

    engine_version = recv_string(sock)

    if __version__ not in engine_version:
        raise ValueError(
            "Version of the API does not match the version of the engine: "
            + __version__
            + " vs. "
            + engine_version
        )


# --------------------------------------------------------------------


def _save_project(name, file_name=None, target_path=None, replace=True):

    # ----------------------------------------------------------------

    if not isinstance(name, str):
        raise TypeError("'name' must be of type str")

    # ----------------------------------------------------------------

    file_name = file_name or name

    if target_path:
        target_path = pathlib.Path(target_path)
    else:
        target_path = pathlib.Path.cwd()

    target_path = target_path.resolve().as_posix()

    cmd = dict()
    cmd["type_"] = "saveproject"
    cmd["body_"] = dict(
        name_=name, file_name_=file_name, target_path_=target_path, replace_=replace
    )

    # ----------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("localhost", tcp_port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(_make_error_msg())

    msg = json.dumps(cmd, cls=_GetmlEncoder)

    send_string(sock, msg)

    # ----------------------------------------------------------------

    msg = log(sock)

    if msg != "Success!":
        engine_exception_handler(msg)

    bundle = recv_string(sock)

    # ----------------------------------------------------------------

    print()
    print(f"Saved project {name} to '{target_path}/{bundle}'")


# --------------------------------------------------------------------


def _set_project(name, restart=False):

    # ----------------------------------------------------------------

    if not isinstance(name, str):
        raise TypeError("'name' must be of type str")

    # ----------------------------------------------------------------

    _check_version()

    # ----------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "setproject"
    cmd["body_"] = name

    # ----------------------------------------------------------------

    if restart:
        cmd["type_"] = "restartproject"

    # ----------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("localhost", tcp_port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(_make_error_msg())

    msg = json.dumps(cmd, cls=_GetmlEncoder)

    send_string(sock, msg)

    # ----------------------------------------------------------------

    msg = log(sock)

    if msg != "Success!":
        engine_exception_handler(msg)

    global port

    port = int(recv_string(sock))

    # ----------------------------------------------------------------

    print()
    print("Connected to project '" + name + "'")


# --------------------------------------------------------------------


def _shutdown():

    # ----------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "shutdownlocal"
    cmd["body_"] = ""

    # ----------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("localhost", tcp_port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(_make_error_msg())

    msg = json.dumps(cmd, cls=_GetmlEncoder)

    send_string(sock, msg)

    # ----------------------------------------------------------------

    sock.close()


# --------------------------------------------------------------------


def _suspend_project(name):

    # ----------------------------------------------------------------

    if not isinstance(name, str):
        raise TypeError("'name' must be of type str")

    # ----------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "suspendproject"
    cmd["body_"] = name

    # ----------------------------------------------------------------

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("localhost", tcp_port))
    except ConnectionRefusedError:
        raise ConnectionRefusedError(_make_error_msg())

    msg = json.dumps(cmd, cls=_GetmlEncoder)

    send_string(sock, msg)

    # ----------------------------------------------------------------

    msg = recv_string(sock)

    if msg != "Success!":
        engine_exception_handler(msg)

    # ----------------------------------------------------------------

    sock.close()
