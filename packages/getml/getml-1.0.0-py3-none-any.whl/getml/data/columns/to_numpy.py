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
Transform column to numpy array
"""


import datetime
import json

import numpy as np

import getml.communication as comm
from getml.constants import TIME_STAMP

from .ts_to_numpy import _ts_to_numpy

def _to_numpy(self, sock=None):
    """
    Transform column to numpy array

    Args:
        sock (optional): Socket connecting the Python API with the getML
            engine.
    """

    # -------------------------------------------
    # Build command string

    cmd = dict()

    cmd["name_"] = ""
    cmd["type_"] = "FloatColumn.get"

    cmd["col_"] = self.cmd

    # -------------------------------------------
    # Establish communication with getml engine

    if sock is None:
        sock2 = comm.send_and_get_socket(cmd)
    else:
        sock2 = sock
        comm.send_string(sock2, json.dumps(cmd))

    msg = comm.recv_string(sock2)

    # -------------------------------------------
    # Make sure everything went well, receive data
    # and close connection

    if msg != "Found!":
        sock2.close()
        comm.engine_exception_handler(msg)

    mat = comm.recv_float_matrix(sock2)

    if sock is None:
        sock2.close()

    # -------------------------------------------

    if TIME_STAMP in self.unit:
        mat = _ts_to_numpy(mat)

    return mat.ravel()
