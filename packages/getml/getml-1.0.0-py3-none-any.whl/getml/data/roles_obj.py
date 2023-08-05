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
Dataclass for handling the roles.
"""

from dataclasses import dataclass, field, fields
from inspect import cleandoc
from typing import List


@dataclass
class Roles:
    """
    Roles can be passed to :class:`~getml.DataFrame` to
    predefine the roles assigned to certain columns.

    Example:
        >>> roles = getml.data.Roles(
        >>>     ...         categorical=["col1", "col2"], target=["col3"])
        >>>
        >>> df_expd = data.DataFrame.from_csv(
                ...         fnames=["file1.csv", "file2.csv"],
                ...         name="MY DATA FRAME",
                ...         sep=';',
                ...         quotechar='"',
                ...         roles=roles
                ... )
    """

    categorical: List[str] = field(default_factory=list)
    join_key: List[str] = field(default_factory=list)
    numerical: List[str] = field(default_factory=list)
    target: List[str] = field(default_factory=list)
    text: List[str] = field(default_factory=list)
    time_stamp: List[str] = field(default_factory=list)
    unused_float: List[str] = field(default_factory=list)
    unused_string: List[str] = field(default_factory=list)

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except TypeError:
            raise KeyError(key)

    def __iter__(self):
        yield from (field_.name for field_ in fields(self))

    def __len__(self):
        return len(fields(self))

    def __repr__(self):
        template = cleandoc(
            """
            {role}:
            - {cols}
            """
        )

        blocks = []

        for role in self:
            if self[role]:
                cols = "\n- ".join(self[role])
                blocks.append(template.format(role=role, cols=cols))

        return "\n\n".join(blocks)

    @property
    def columns(self):
        """
        The name of all columns contained in the roles object.
        """
        return [r for role in self for r in self[role]]

    def infer(self, colname):
        """
        Infers the role of a column.

        Args:
            colname (str):
                The name of the column to be inferred.
        """
        for role in self:
            if colname in self[role]:
                return role
        raise ValueError("Column named '" + colname + "' not found.")

    def to_dict(self):
        """
        Expresses the roles object as a dictionary.
        """
        return {role: self[role] for role in self}

    def to_list(self):
        """
        Returns a list containing the roles, without the corresponding
        columns names.
        """
        return [r for role in self for r in [role] * len(self[role])]

    @property
    def unused(self):
        """
        Names of all unused columns (unused_float + unused_string).
        """
        return self.unused_float + self.unused_string
