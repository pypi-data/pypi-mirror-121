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
Custom class for handling the columns of a pipeline.
"""

import json
import numbers
import re
from copy import deepcopy

import numpy as np
import pandas as pd  # type: ignore

import getml.communication as comm
from getml.data import Container, StarSchema, TimeSeries
from getml.data.helpers import _is_typed_list
from getml.utilities.formatting import _Formatter

from .column import Column
from .helpers import PERIPHERAL, POPULATION, _drop


class Columns:
    """
    Container which holds a pipeline's columns. Columns can be accessed
    by name, index or with a numpy array. The container supports slicing and
    is sort- and filterable.

    Further, the container holds global methods to request columns' importances
    and apply a column selection to data frames provided to the pipeline.

    Note:
        The container is an iterable. So, in addition to
        :meth:`~getml.pipeline.Columns.filter` you can also use python list
        comprehensions for filtering.

    Example:
        .. code-block:: python

            all_my_columns = my_pipeline.columns

            first_column = my_pipeline.columns[0]

            all_but_last_10_columns = my_pipeline.columns[:-10]

            important_columns = [column for column in my_pipeline.columns if column.importance > 0.1]

            names, importances = my_pipeline.columns.importances()

            # Drops all categorical and numerical columns that are not
            # in the top 20%.
            new_container = my_pipeline.columns.select(
                container,
                share_selected_columns=0.2,
            )
    """

    # ----------------------------------------------------------------

    def __init__(self, pipeline, targets, peripheral, data=None):

        if not isinstance(pipeline, str):
            raise ValueError("'pipeline' must be a str.")

        if not _is_typed_list(targets, str):
            raise TypeError("'targets' must be a list of str.")

        self.pipeline = pipeline

        self.targets = targets

        self.peripheral = peripheral

        self.peripheral_names = [p.name for p in self.peripheral]

        if data is None:
            self.data = self._load_columns()
        else:
            self.data = data

    # ----------------------------------------------------------------

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.data[key]
        if isinstance(key, slice):
            columns_subset = self.data[key]
            return self._make_columns(columns_subset)
        if isinstance(key, str):
            if key in self.names:
                return [column for column in self.data if column.name == key][0]
            raise AttributeError(f"No Column with name: {key}")
        if isinstance(key, np.ndarray):
            columns_subset = np.array(self.data)[key].tolist()
            return columns_subset
        raise TypeError(
            f"Columns can only be indexed by: int, slices, or str, not {type(key).__name__}"
        )

    # ----------------------------------------------------------------

    def __repr__(self):
        return self._format()._render_string()

    # ------------------------------------------------------------

    def _repr_html_(self):
        return self._format()._render_html()

    # ----------------------------------------------------------------

    def _get_column_importances(self, target_num, sort):

        cmd = dict()

        cmd["type_"] = "Pipeline.column_importances"
        cmd["name_"] = self.pipeline

        cmd["target_num_"] = target_num

        # ------------------------------------------------------------

        sock = comm.send_and_get_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Success!":
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        msg = comm.recv_string(sock)

        json_obj = json.loads(msg)

        # ------------------------------------------------------------

        descriptions = np.asarray(json_obj["column_descriptions_"])
        importances = np.asarray(json_obj["column_importances_"])

        # ------------------------------------------------------------

        if hasattr(self, "data"):
            indices = np.asarray(
                [
                    column.index
                    for column in self.data
                    if column.target == self.targets[target_num]
                    and column.index < len(importances)
                ]
            )

            descriptions = descriptions[indices]
            importances = importances[indices]
        # ------------------------------------------------------------

        if not sort:
            return descriptions, importances

        # ------------------------------------------------------------

        indices = np.argsort(importances)[::-1]

        # ------------------------------------------------------------

        return (descriptions[indices], importances[indices])

    # ----------------------------------------------------------------

    def _format(self):
        rows = [
            [
                column.name,
                column.marker,
                column.table,
                column.importance,
                column.target,
            ]
            for column in self.data
        ]

        headers = [
            [
                "name",
                "marker",
                "table",
                "importance",
                "target",
            ]
        ]

        return _Formatter(headers, rows)

    # ----------------------------------------------------------------

    def _load_columns(self):
        """
        Loads the actual column data from the engine.
        """
        columns = []

        for target_num, target in enumerate(self.targets):
            descriptions, importances = self._get_column_importances(
                target_num=target_num, sort=False
            )

            columns.extend(
                [
                    Column(
                        index=index,
                        name=description.get("name_"),
                        marker=description.get("marker_"),
                        table=description.get("table_"),
                        importance=importances[index],
                        target=target,
                    )
                    for index, description in enumerate(descriptions)
                ]
            )

        return columns

    # ----------------------------------------------------------------

    def _make_columns(self, data):
        """
        A factory to construct a :class:`getml.pipeline.Columns` container from a list of
        :class:`getml.pipeline.Column`s.
        """
        return Columns(self.pipeline, self.targets, self.peripheral, data)

    # ----------------------------------------------------------------

    def _pivot(self, field):
        """
        Pivots the data for a given field. Returns a list of values of the field's type.
        """
        return [getattr(column, field) for column in self.data]

    # ----------------------------------------------------------------

    def filter(self, conditional):
        """
        Filters the columns container.

        Args:
            conditional (callable, optional):
                A callable that evaluates to a boolean for a given item.

        Return:
            :class:`getml.pipeline.Column`:
                A container of filtered Columns.

        Example:
            .. code-block:: python

                important_columns = my_pipeline.columns.filter(lambda column: column.importance > 0.1)

                peripheral_columns = my_pipeline.columns.filter(lambda column: column.marker == "[PERIPHERAL]")

        """
        columns_filtered = [column for column in self.data if conditional(column)]
        return self._make_columns(columns_filtered)

    # ----------------------------------------------------------------

    def importances(self, target_num=0, sort=True):
        """
        Returns the data for the column importances.

        Column importances extend the idea of column importances
        to the columns originally inserted into the pipeline.
        Each column is assigned an importance value that measures
        its contribution to the predictive performance. All
        columns importances add up to 1.

        Args:
            target_num (int):
                Indicates for which target you want to view the
                importances.
                (Pipelines can have more than one target.)

            sort (bool):
                Whether you want the results to be sorted.

        Return:
            (:class:`numpy.ndarray`, :class:`numpy.ndarray`):
                - The first array contains the names of
                  the columns.
                - The second array contains their importances.
                  By definition, all importances add up to 1.
        """

        # ------------------------------------------------------------

        descriptions, importances = self._get_column_importances(
            target_num=target_num, sort=sort
        )

        # ------------------------------------------------------------

        names = np.asarray(
            [d["marker_"] + " " + d["table_"] + "." + d["name_"] for d in descriptions]
        )

        # ------------------------------------------------------------

        return names, importances

    # ----------------------------------------------------------------

    @property
    def names(self):
        """
        Holds the names of a :class:`~getml.Pipeline`\'s columns.

        Returns:
            :class:`list` containing the names.

        Note:

            The order corresponds to the current sorting of the container.
        """
        return [column.name for column in self.data]

    # ----------------------------------------------------------------

    def select(self, container, share_selected_columns=0.5):
        """
        Returns a new data container with all insufficiently important columns dropped.

        Args:
            container (:class:`getml.data.Container` or :class:`getml.data.StarSchema` or :class:`getml.data.TimeSeries`):
                The container containing the data you want to use.

            share_selected_columns(numerical): The share of columns
                to keep. Must be between 0.0 and 1.0.
        """

        # ------------------------------------------------------------

        if isinstance(container, (StarSchema, TimeSeries)):
            data = self.select(
                container.container, share_selected_columns=share_selected_columns
            )
            new_container = deepcopy(container)
            new_container._container = data
            return new_container

        # ------------------------------------------------------------

        if not isinstance(container, Container):
            raise TypeError(
                "'container' must be a getml.data.Container, "
                + "a getml.data.StarSchema or a getml.data.TimeSeries"
            )

        if not isinstance(share_selected_columns, numbers.Real):
            raise TypeError("'share_selected_columns' must be a real number!")

        if share_selected_columns < 0.0 or share_selected_columns > 1.0:
            raise ValueError("'share_selected_columns' must be between 0 and 1!")

        # ------------------------------------------------------------

        descriptions, _ = self._get_column_importances(target_num=-1, sort=True)

        # ------------------------------------------------------------

        num_keep = int(np.ceil(share_selected_columns * len(descriptions)))

        keep_columns = descriptions[:num_keep]

        # ------------------------------------------------------------

        subsets = {
            k: _drop(v, keep_columns, k, POPULATION)
            for (k, v) in container.subsets.items()
        }

        peripheral = {
            k: _drop(v, keep_columns, k, PERIPHERAL)
            for (k, v) in container.peripheral.items()
        }

        # ------------------------------------------------------------

        new_container = Container(**subsets)
        new_container.add(**peripheral)
        new_container.freeze()

        # ------------------------------------------------------------

        return new_container

    # ----------------------------------------------------------------

    def sort(self, by=None, key=None, descending=None):
        """
        Sorts the Columns container. If no arguments are provided the
        container is sorted by target and name.

        Args:
            by (str, optional):
                The name of field to sort by. Possible fields:
                    - name(s)
                    - table(s)
                    - importances(s)
            key (callable, optional):
                A callable that evaluates to a sort key for a given item.
            descending (bool, optional):
                Whether to sort in descending order.

        Return:
            :class:`getml.pipeline.columns`:
                A container of sorted columns.

        Example:
            .. code-block:: python

                by_importance = my_pipeline.columns.sort(key=lambda column: column.importance)

        """

        reverse = descending or False

        if (by is not None) and (key is not None):
            raise ValueError("Only one of `by` and `key` can be provided.")

        if key is not None:
            columns_sorted = sorted(self.data, key=key, reverse=reverse)
            return self._make_columns(columns_sorted)

        if by is None:
            columns_sorted = sorted(
                self.data, key=lambda column: column.name, reverse=reverse
            )
            columns_sorted.sort(key=lambda column: column.target)
            return self._make_columns(columns_sorted)

        if re.match(by, "names?"):
            columns_sorted = sorted(
                self.data, key=lambda column: column.name, reverse=reverse
            )
            return self._make_columns(columns_sorted)

        if re.match(by, "tables?"):
            columns_sorted = sorted(
                self.data,
                key=lambda column: column.table,
            )
            return self._make_columns(columns_sorted)

        if re.match(by, "importances?"):
            reverse = descending or True
            columns_sorted = sorted(
                self.data, key=lambda column: column.importance, reverse=reverse
            )
            return self._make_columns(columns_sorted)

        raise ValueError(f"Cannot sort by: {by}.")

    # ----------------------------------------------------------------

    def to_pandas(self):
        """Returns all information related to the columns in a pandas data frame."""

        names, markers, tables, importances, targets = (
            self._pivot(field)
            for field in ["name", "marker", "table", "importance", "target"]
        )

        data_frame = pd.DataFrame(index=np.arange(len(self.data)))

        data_frame["name"] = names

        data_frame["marker"] = markers

        data_frame["table"] = tables

        data_frame["importance"] = importances

        data_frame["target"] = targets

        return data_frame

    # ----------------------------------------------------------------
