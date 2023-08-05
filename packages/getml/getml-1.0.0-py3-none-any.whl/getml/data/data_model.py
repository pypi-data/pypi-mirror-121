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
A container for the placeholders.
"""

from copy import deepcopy

from getml.utilities.formatting import _Formatter

from .diagram import _Diagram
from .helpers import _is_typed_list
from .placeholder import Placeholder
from .staging import _make_staging_overview


class DataModel:
    """Abstract representation of the relationship between tables.

    You might also want to refer to :class:`~getml.data.Placeholder`.

    Args:
        population (:class:`~getml.data.Placeholder`):
            The placeholder representing the population table,
            which defines the
            `statistical population <https://en.wikipedia.org/wiki/Statistical_population>`_
            and contains the targets.

    Examples:
        This example will construct a data model in which the
        'population_table' depends on the 'peripheral_table' via
        the 'join_key' column. In addition, only those rows in
        'peripheral_table' for which 'time_stamp' is smaller or
        equal to the 'time_stamp' in 'population_table' are considered:

        .. code-block:: python

            dm = getml.data.DataModel(
                population_table.to_placeholder("POPULATION")
            )

            dm.add(peripheral_table.to_placeholder("PERIPHERAL"))

            dm.POPULATION.join(
                dm.PERIPHERAL,
                on="join_key",
                time_stamps="time_stamp"
            )

        If you want to add more than one peripheral table, you can
        use :func:`~getml.data.to_placeholder`:

        .. code-block:: python

            dm = getml.data.DataModel(
                population_table.to_placeholder("POPULATION")
            )

            dm.add(
                getml.data.to_placeholder(
                    PERIPHERAL1=peripheral_table_1,
                    PERIPHERAL2=peripheral_table_2,
                )
            )

        If the relationship between two tables is many-to-one or one-to-one
        you should clearly say so:

        .. code-block:: python

            dm.POPULATION.join(
                dm.PERIPHERAL,
                on="join_key",
                time_stamps="time_stamp",
                relationship=getml.data.relationship.many_to_one,
            )

        Please also refer to :mod:`~getml.data.relationship`.

        If the join keys or time stamps are named differently in the two
        different tables, use a tuple:

        .. code-block:: python

            dm.POPULATION.join(
                dm.PERIPHERAL,
                on=("join_key", "other_join_key"),
                time_stamps=("time_stamp", "other_time_stamp"),
            )

        You can join over more than one join key:

        .. code-block:: python

            dm.POPULATION.join(
                dm.PERIPHERAL,
                on=["join_key1", "join_key2", ("join_key3", "other_join_key3")],
                time_stamps="time_stamp",
            )

        You can also limit the scope of your joins using *memory*. This
        can significantly speed up training time. For instance, if you
        only want to consider data from the last seven days, you could
        do something like this:

        .. code-block:: python

            dm.POPULATION.join(
                dm.PERIPHERAL,
                on="join_key",
                time_stamps="time_stamp",
                memory=getml.data.time.days(7),
            )

        In some use cases, particularly those involving time series, it
        might be a good idea to use targets from the past. You can activate
        this using *lagged_targets*. But if you do that, you must
        also define a prediction *horizon*. For instance, if you want to
        predict data for the next hour, using data from the last seven days,
        you could do this:

        .. code-block:: python

            dm.POPULATION.join(
                dm.PERIPHERAL,
                on="join_key",
                time_stamps="time_stamp",
                lagged_targets=True,
                horizon=getml.data.time.hours(1),
                memory=getml.data.time.days(7),
            )

        Please also refer to :mod:`~getml.data.time`.

        If the join involves many matches, it might be a good idea to set the
        relationship to :const:`~getml.data.relationship.propositionalization`.
        This forces the pipeline to always use a propositionalization
        algorithm for this join, which can significantly speed things up.

        .. code-block:: python

            dm.POPULATION.join(
                dm.PERIPHERAL,
                on="join_key",
                time_stamps="time_stamp",
                relationship=getml.data.relationship.propositionalization,
            )

        Please also refer to :mod:`~getml.data.relationship`.

        In some cases, it is necessary to have more than one placeholder
        on the same table. This is necessary to create more complicated
        data models. In this case, you can do something like this:

        .. code-block:: python

            dm.add(
                getml.data.to_placeholder(
                    PERIPHERAL=[peripheral_table]*2,
                )
            )

            # We can now access our two placeholders like this:
            placeholder1 = dm.PERIPHERAL[0]
            placeholder2 = dm.PERIPHERAL[1]

        If you want to check out a real-world example where this
        is necessary, refer to the
        `CORA notebook <https://nbviewer.getml.com/github/getml/getml-demo/blob/master/cora.ipynb>`_.
    """

    def __init__(self, population):

        if isinstance(population, str):
            population = Placeholder(population)

        if not isinstance(population, Placeholder):
            raise TypeError(
                "'population' must be a getml.data.Placeholder or a str, got "
                + type(population).__name__
                + "."
            )

        self.population = population

        self.peripheral = {}

    def _add(self, placeholder):

        if placeholder.name in self.peripheral:
            try:
                self.peripheral[placeholder.name].append(placeholder)
            except AttributeError:
                self.peripheral[placeholder.name] = [
                    self.peripheral[placeholder.name],
                    placeholder,
                ]
        else:
            self.peripheral.update({placeholder.name: placeholder})

    def __dir__(self):
        attrs = dir(type(self)) + list(vars(self))
        attrs.extend(self.names)
        return attrs

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            super().__getattribute__(key)

    def __getitem__(self, key):
        population = vars(self)["population"]
        peripheral = vars(self)["peripheral"]

        phs = {
            "population": population,
            population.name: population,
            **peripheral,
        }

        return phs[key]

    def _getml_deserialize(self):
        def deserialize(elem):
            return (
                [e._getml_deserialize() for e in elem]
                if isinstance(elem, list)
                else elem._getml_deserialize()
            )

        cmd = self.population._getml_deserialize()
        cmd["peripheral_"] = {k: deserialize(v) for (k, v) in self.peripheral.items()}
        return cmd

    def __iter__(self):
        yield from [self.population.name] + ["population"] + list(self.peripheral)

    def __repr__(self):
        return "\n\n".join(repr(ph) for ph in self.population.to_list())

    def _make_diagram(self):
        return (
            "<div style='margin-top: 15px;'><h4>diagram</h4><br>"
            + _Diagram(self.population).to_html()
            + "</div>"
        )

    def _make_staging(self):
        headers = [["data frames", "staging table"]]
        rows = _make_staging_overview(self.population)
        staging_table = _Formatter(headers=headers, rows=rows)._render_html()
        return (
            "<div style='margin-top: 15px;'><h4>staging</h4>" + staging_table + "</div>"
        )

    def _repr_html_(self):
        return self._make_diagram() + "<br><br>" + self._make_staging()

    def add(self, *placeholders):
        """
        Adds peripheral placeholders to the data model.

        Args:
            placeholders (:class:`~getml.data.Placeholder`):
                The placeholder or placeholders you would like to add.
        """

        def to_list(elem):
            return elem if isinstance(elem, list) else [elem]

        # We want to be 100% sure that all handles are unique,
        # so we need deepcopy.
        placeholders = [deepcopy(ph) for elem in placeholders for ph in to_list(elem)]

        if not _is_typed_list(placeholders, Placeholder):
            raise TypeError(
                "'placeholders' must consist of getml.data.Placeholders "
                + "or lists thereof."
            )

        for placeholder in placeholders:
            self._add(placeholder)

    @property
    def names(self):
        """
        A list of the names of all tables contained in the DataModel.
        """
        return [name for name in self]
