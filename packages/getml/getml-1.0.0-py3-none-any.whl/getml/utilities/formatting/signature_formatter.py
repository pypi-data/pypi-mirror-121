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
Holds the SignatureFormatter class that allows for the proper formatting of function and
class signatures.
"""

from copy import deepcopy

from .formatter import _truncate_line

# --------------------------------------------------------------------

STYLE = "pep8"

# --------------------------------------------------------------------


def _split_value(value, start, max_width):
    split = []

    if isinstance(value, list):
        truncated = list(_truncate_line(value, 2, max_width - start, template="{!r}"))
        remaining = value[len(truncated) :]
        split.append(truncated)

        if remaining:
            split.extend(_split_value(remaining, start, max_width))

        return split

    return value


# --------------------------------------------------------------------


def _format_list(values, indent, value_indent, template):
    values_formatted = [", ".join(f"{elem!r}" for elem in line) for line in values]
    indentation = " " * (indent + value_indent)
    lines_formatted = f",\n{indentation}".join(values_formatted)
    return template.format(lines_formatted)


# --------------------------------------------------------------------


def _remove_private(dict):
    return {key: val for key, val in dict.items() if key[0] != "_"}


# --------------------------------------------------------------------


class _SignatureFormatter:
    """
    A formatter for function and class signatures. Used for generating appropriate
    __repr__s.

    Outputs a PEP8-compliant string representation of a signature with a maximum of one
    argument per line. Lists of parameter values that exceed a given width are splitted
    to span multiple lines, while preserving proper indendation.
    """

    max_width = 88
    value_indent = 4

    # ------------------------------------------------------------

    def __init__(self, obj=None, data=None):
        if obj and not data:
            self.data = vars(obj)
            self.type = type(obj).__name__
        elif data and not obj:
            data = deepcopy(data)
            self.type = data.pop("type")
            self.data = data
        else:
            raise TypeError("Can construct signatures only from one of object or dict.")

        self.data = _remove_private(self.data)

        self.template = f"{self.type}" "({})"
        self.indent = len(self.template[:-3])

    # ------------------------------------------------------------

    def _format_pep8(self, suppress_none=False):
        params_formatted = []

        for name, value in self.data.items():
            if suppress_none and value is None:
                continue

            if (
                isinstance(value, list)
                and self.indent + len(f"{name}={value!r}") > self.max_width
            ):
                list_split = _split_value(
                    value,
                    start=self.indent + self.value_indent,
                    max_width=self.max_width,
                )

                list_template = "[{}]"

                value_formatted = _format_list(
                    list_split,
                    self.indent,
                    len(name) + 2,
                    list_template,
                )

            else:
                value_formatted = f"{value!r}"

            params_formatted.append(f"{name}={value_formatted}")

        return self.template.format(f",\n{self.indentation}".join(params_formatted))

    # ------------------------------------------------------------

    def _format_black(self, suppress_none=False):

        if len(self.params_formatted) + self.value_indent < self.max_width:
            return self.template.format(
                f"\n{self.value_indentation}" + self.params_formatted + "\n"
            )

        params_formatted = []

        for name, value in self.data.items():
            if suppress_none and value is None:
                continue
            if len(f"{name}={value}") > self.max_width:
                list_split = [[elem] for elem in value]

                list_template = (
                    f"[\n{self.value_indentation * 2}{{}},\n{self.value_indentation}]"
                )

                value_formatted = _format_list(
                    list_split, self.value_indent, self.value_indent, list_template
                )

            else:
                value_formatted = f"{value!r}"

            params_formatted.append(f"{name}={value_formatted}")

        return self.template.format(
            f"\n{self.value_indentation}"
            + f",\n{self.value_indentation}".join(params_formatted)
            + "\n"
        )

    # ------------------------------------------------------------

    def _format_compact(self, suppress_none=False):

        # tokenize params regardless of of parameter values' depth by splitting
        # params formatted as a single line string on ", "
        params_tokenized = self.params_formatted.split(", ", suppress_none)

        params_split = _split_value(
            params_tokenized, start=self.indent, max_width=self.max_width
        )

        params_formatted = f",\n{self.indentation}".join(
            ", ".join(elem for elem in line) for line in params_split
        )

        return self.template.format(params_formatted)

    # ------------------------------------------------------------

    def _format(self, suppress_none=False, style=None):

        style = style or STYLE

        one_line = self.template.format(self.params_formatted, suppress_none)
        if len(one_line) < self.max_width:
            return one_line

        styles = [attr[8:] for attr in vars(type(self)) if attr.startswith("_format_")]

        if style in styles:
            return getattr(self, "_format_" + style)(suppress_none)

        raise AttributeError(
            f"No format style: {style}. Choose one of: {', '.join(styles)}"
        )

    # ------------------------------------------------------------

    @property
    def indentation(self):
        return " " * self.indent

    # ------------------------------------------------------------

    @property
    def value_indentation(self):
        return " " * self.value_indent

    # ------------------------------------------------------------

    @property
    def params_formatted(self):
        return ", ".join(
            f"{name}={value!r}"
            for name, value in self.data.items()
            if value is not None
        )
