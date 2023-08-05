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
Columns marked with a subrole in this submodule will not be used
for the specified purpose.

Example:
    .. code-block:: python

        # The Relboost feature learning algorithm will
        # ignore this column.
        my_data_frame.set_subroles(
            "my_column", getml.data.subroles.exclude.relboost)
"""

fastprop = "exclude fastprop"
"""
:class:`~getml.feature_learning.FastProp` will ignore
this column.
"""


feature_learners = "exclude feature learners"
"""
All feature learners (:mod:`~getml.feature_learning`)
will ignore this column.
"""

imputation = "exclude imputation"
"""
The :class:`~getml.preprocessors.Imputation` preprocessor
will ignore this column.
"""

mapping = "exclude mapping"
"""
The :class:`~getml.preprocessors.Mapping` preprocessor
will ignore this column.
"""

multirel = "exclude multirel"
"""
:class:`~getml.feature_learning.Multirel` will ignore
this column.
"""

predictors = "exclude predictors"
"""
All :mod:`~getml.predictors` will ignore this column.
"""

preprocessors = "exclude preprocessors"
"""
All :mod:`~getml.preprocessors` will ignore this column.
"""

relboost = "exclude relboost"
"""
:class:`~getml.feature_learning.Relboost` will ignore
this column.
"""

relmt = "exclude relmt"
"""
:class:`~getml.feature_learning.RelMT` will ignore
this column.
"""

seasonal = "exclude seasonal"
"""
The :class:`~getml.preprocessors.Seasonal` preprocessor
will ignore this column.
"""

text_field_splitter = "exclude text field splitter"
"""
The :class:`~getml.preprocessors.TextFieldSplitter`
will ignore this column.
"""

__all__ = ("fastprop", "feature_learners", "imputation", "mapping", "multirel",
           "predictors", "preprocessors", "relboost", "relmt",
           "seasonal", "text_field_splitter")

_all_exclude = [fastprop, feature_learners, imputation, mapping, multirel,
                predictors, preprocessors, relboost,
                relmt, seasonal, text_field_splitter]
