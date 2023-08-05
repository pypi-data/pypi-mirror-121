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

import json

import getml.communication as comm
from getml.data.columns import _parse

from .container import Container
from .helpers2 import _load_view

"""Load a container."""


def load_container(container_id):
    """
    Loads a container and all associated data frames from disk.

    Args:
        container_id (str):
            The id of the container you would like to load.
    """

    # -----------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "DataContainer.load"
    cmd["name_"] = container_id

    sock = comm.send_and_get_socket(cmd)

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    json_str = comm.recv_string(sock)

    cmd = json.loads(json_str)

    # -----------------------------------------------------------------

    population = _load_view(
        cmd["population_"]) if "population_" in cmd else None

    peripheral = {k: _load_view(v) for (k, v) in cmd["peripheral_"].items()}

    subsets = {k: _load_view(v) for (k, v) in cmd["subsets_"].items()}

    split = _parse(cmd["split_"]) if "split_" in cmd else None

    deep_copy = cmd["deep_copy_"]
    frozen_time = cmd["frozen_time_"] if "frozen_time_" in cmd else None
    last_change = cmd["last_change_"]

    container = Container(
        population=population, peripheral=peripheral, deep_copy=deep_copy, **subsets
    )

    container._id = container_id
    container._frozen_time = frozen_time
    container._split = split
    container._last_change = last_change

    return container
