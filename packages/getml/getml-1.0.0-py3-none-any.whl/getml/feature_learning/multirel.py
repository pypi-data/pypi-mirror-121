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
Feature learning based on Multi-Relational Decision Tree Learning.
"""

from dataclasses import dataclass, field
from typing import ClassVar, List, Union

from .aggregations import _Aggregations
from .aggregations import multirel as multirel_aggregations
from .fastprop import FastProp
from .feature_learner import _FeatureLearner
from .validation import _validate_multirel_parameters

# --------------------------------------------------------------------


@dataclass(repr=False)
class Multirel(_FeatureLearner):
    """Feature learning based on Multi-Relational Decision Tree Learning.

    :class:`~getml.feature_learning.Multirel` automates feature learning
    for relational data and time series. It is based on an efficient
    variation of the Multi-Relational Decision Tree Learning (MRDTL).

    For more information on the underlying feature learning algorithm, check
    out the :ref:`User guide <feature_learning_algorithms_multirel>`.

    Args:
        aggregation (List[:class:`~getml.feature_learning.aggregations`], optional):
            Mathematical operations used by the automated feature
            learning algorithm to create new features.

            Must be from :mod:`~getml.feature_learning.aggregations`.

        allow_sets (bool, optional):
            Multirel can summarize different categories into sets for
            producing conditions. When expressed as SQL statements these
            sets might look like this:

            .. code-block:: sql

                t2.category IN ( 'value_1', 'value_2', ... )

            This can be very powerful, but it can also produce
            features that are hard to read and might be prone to
            overfitting when the `sampling_factor` is too low.

        delta_t (float, optional):
            Frequency with which lag variables will be explored in a
            time series setting. When set to 0.0, there will be no lag
            variables.

            For more information please refer to
            :ref:`data_model_time_series`. Range: [0, :math:`\\infty`]

        grid_factor (float, optional):
            Multirel will try a grid of critical values for your
            numerical features. A higher `grid_factor` will lead to a
            larger number of critical values being considered. This
            can increase the training time, but also lead to more
            accurate features. Range: (0, :math:`\\infty`]

        loss_function (:class:`~getml.feature_learning.loss_functions`, optional):
            Objective function used by the feature learning algorithm
            to optimize your features. For regression problems use
            :class:`~getml.feature_learning.loss_functions.SquareLoss` and for
            classification problems use
            :class:`~getml.feature_learning.loss_functions.CrossEntropyLoss`.

        max_length (int, optional):
            The maximum length a subcondition might have. Multirel
            will create conditions in the form

            .. code-block:: sql

                (condition 1.1 AND condition 1.2 AND condition 1.3 )
                OR ( condition 2.1 AND condition 2.2 AND condition 2.3 )
                ...

            Using this parameter you can set the maximum number of
            conditions allowed in the brackets. Range: [0, :math:`\\infty`]

        min_df (int, optional):
            Only relevant for columns with role :const:`~getml.data.roles.text`.
            The minimum
            number of fields (i.e. rows) in :const:`~getml.data.roles.text` column a
            given word is required to appear in to be included in the bag of words.
            Range: [1, :math:`\\infty`]

        min_num_samples (int, optional):
            Determines the minimum number of samples a subcondition
            should apply to in order for it to be considered. Higher
            values lead to less complex statements and less danger of
            overfitting. Range: [1, :math:`\\infty`]

        num_features (int, optional):
            Number of features generated by the feature learning
            algorithm. Range: [1, :math:`\\infty`]

        num_subfeatures (int, optional):
            The number of subfeatures you would like to extract in a
            subensemble (for snowflake data model only). See
            :ref:`data_model_snowflake_schema` for more
            information. Range: [1, :math:`\\infty`]

        num_threads (int, optional):
            Number of threads used by the feature learning algorithm. If set to
            zero or a negative value, the number of threads will be
            determined automatically by the getML engine. Range:
            [:math:`0`, :math:`\\infty`]

        propositionalization (:class:`~getml.feature_learning.FastProp`, optional):
            The feature learner used for joins which are flagged to be
            propositionalized (by setting a join's `relationship` parameter to
            :const:`getml.data.relationship.propositionalization`)

        regularization (float, optional):
            Most important regularization parameter for the quality of
            the features produced by Multirel. Higher values will lead
            to less complex features and less danger of overfitting. A
            `regularization` of 1.0 is very strong and allows no
            conditions. Range: [0, 1]

        round_robin (bool, optional):
            If True, the Multirel picks a different `aggregation`
            every time a new feature is generated.

        sampling_factor (float, optional):
            Multirel uses a bootstrapping procedure (sampling with
            replacement) to train each of the features. The sampling
            factor is proportional to the share of the samples
            randomly drawn from the population table every time
            Multirel generates a new feature. A lower sampling factor
            (but still greater than 0.0), will lead to less danger of
            overfitting, less complex statements and faster
            training. When set to 1.0, roughly 20,000 samples are drawn
            from the population table. If the population table
            contains less than 20,000 samples, it will use standard
            bagging. When set to 0.0, there will be no sampling at
            all. Range: [0, :math:`\\infty`]

        seed (Union[int,None], optional):
            Seed used for the random number generator that underlies
            the sampling procedure to make the calculation
            reproducible. Internally, a `seed` of None will be mapped to
            5543. Range: [0, :math:`\\infty`]

        share_aggregations (float, optional):
            Every time a new feature is generated, the `aggregation`
            will be taken from a random subsample of possible
            aggregations and values to be aggregated. This parameter
            determines the size of that subsample. Only relevant when
            `round_robin` is False. Range: [0, 1]

        share_conditions (float, optional):
            Every time a new column is tested for applying conditions,
            it might be skipped at random. This parameter determines
            the probability that a column will *not* be
            skipped. Range: [0, 1]

        shrinkage (float, optional):
            Since Multirel works using a gradient-boosting-like
            algorithm, `shrinkage` (or learning rate) scales down the
            weights and thus the impact of each new tree. This gives
            more room for future ones to improve the overall
            performance of the model in this greedy algorithm. Higher
            values will lead to more danger of overfitting. Range: [0,
            1]

        silent (bool, optional):
            Controls the logging during training.

        vocab_size (int, optional):
            Determines the maximum number
            of words that are extracted in total from :const:`getml.data.roles.text`
            columns. This can be interpreted as the maximum size of the bag of words.
            Range: [0, :math:`\\infty`]
    """

    # ----------------------------------------------------------------

    agg_sets: ClassVar[_Aggregations] = multirel_aggregations

    # ----------------------------------------------------------------

    aggregation: List[str] = field(
        default_factory=lambda: multirel_aggregations.Default
    )
    allow_sets: bool = True
    delta_t: float = 0.0
    grid_factor: float = 1.0
    loss_function: Union[str, None] = None
    max_length: int = 4
    min_df: int = 30
    min_num_samples: int = 1
    num_features: int = 100
    num_subfeatures: int = 5
    num_threads: int = 0
    propositionalization: FastProp = FastProp()
    regularization: float = 0.01
    round_robin: bool = False
    sampling_factor: float = 1.0
    seed: int = 5543
    share_aggregations: float = 0.0
    share_conditions: float = 1.0
    shrinkage: float = 0.0
    silent: bool = True
    vocab_size: int = 500

    # ----------------------------------------------------------------

    def validate(self, params=None):
        """Checks both the types and the values of all instance
        variables and raises an exception if something is off.

        Args:
            params (dict, optional): A dictionary containing
                the parameters to validate. If not is passed,
                the own parameters will be validated.
        """

        # ------------------------------------------------------------

        if params is None:
            params = self.__dict__
        else:
            params = {**self.__dict__, **params}

        # ------------------------------------------------------------

        if not isinstance(params, dict):
            raise ValueError("params must be None or a dictionary!")

        # ------------------------------------------------------------

        for kkey in params:
            if kkey not in type(self)._supported_params:
                raise KeyError(
                    f"Instance variable '{kkey}' is not supported in {self.type}."
                )

        # ------------------------------------------------------------

        _validate_multirel_parameters(**params)


# --------------------------------------------------------------------
