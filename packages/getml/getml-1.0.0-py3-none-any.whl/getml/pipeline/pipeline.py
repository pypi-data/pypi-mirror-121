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
This submodule contains the Pipeline, which is the main
class for feature learning and prediction.
"""

import copy
import json
import numbers
import socket
import time
from datetime import datetime

import numpy as np

import getml.communication as comm
from getml import data
from getml.data import DataModel, _decode_data_model, _decode_placeholder
from getml.data.helpers import (
    _is_subclass_list,
    _is_typed_list,
    _remove_trailing_underscores,
)
from getml.feature_learning import _FeatureLearner
from getml.feature_learning.loss_functions import _classification_loss
from getml.predictors import _classification_types, _Predictor
from getml.preprocessors.preprocessor import _Preprocessor
from getml.utilities.formatting import _SignatureFormatter

from .columns import Columns
from .features import Features
from .helpers import (
    _check_df_types,
    _handle_loss_function,
    _infer_peripheral,
    _make_id,
    _parse_fe,
    _parse_pred,
    _parse_preprocessor,
    _print_time_taken,
    _replace_with_nan_maybe,
    _transform_peripheral,
)
from .metrics import (
    _all_metrics,
    _classification_metrics,
    accuracy,
    auc,
    cross_entropy,
    mae,
    rmse,
    rsquared,
)
from .plots import Plots
from .score import ClassificationScore, RegressionScore
from .scores_container import Scores
from .tags import Tags

# --------------------------------------------------------------------

NOT_FITTED = "NOT FITTED"


class Pipeline:
    """
    A Pipeline is the main class for feature learning and prediction.

    Args:
        data_model (:class:`~getml.data.DataModel`):
            Abstract representation of the data_model,
            which defines the abstract relationships between the tables.
            Required for the feature learners.

        peripheral (Union[:class:`~getml.data.Placeholder`, List[:class:`~getml.data.Placeholder`]], optional):
            Abstract representations of the additional tables used to
            augment the information provided in `population`. These
            have to be the same objects that were
            :meth:`~getml.data.Placeholder.join` ed onto the
            `population` :class:`~getml.data.Placeholder`.
            Their order determines the order of the
            peripheral :class:`~getml.DataFrame` passed to
            the 'peripheral_tables' argument in
            :meth:`~getml.Pipeline.check`,
            :meth:`~getml.Pipeline.fit`,
            :meth:`~getml.Pipeline.predict`,
            :meth:`~getml.Pipeline.score`, and
            :meth:`~getml.Pipeline.transform`, if you
            pass the data frames as a list.
            If you omit the peripheral placeholders, they will
            be inferred from the data model and ordered
            alphabetically.

        preprocessors (Union[:class:`~getml.feature_learning._Preprocessor`, List[:class:`~getml.feature_learning._Preprocessor`]], optional):
            The preprocessor(s) to be used.
            Must be from :mod:`~getml.preprocessors`.
            A single preprocessor does not have to be wrapped in a list.

        feature_learners (Union[:class:`~getml.feature_learning._FeatureLearner`, List[:class:`~getml.feature_learning._FeatureLearner`]], optional):
            The feature learner(s) to be used.
            Must be from :mod:`~getml.feature_learning`.
            A single feature learner does not have to be wrapped
            in a list.

        feature_selectors (Union[:class:`~getml.predictors._Predictor`, List[:class:`~getml.predictors._Predictor`]], optional):
            Predictor(s) used to select the best features.
            Must be from :mod:`~getml.predictors`.
            A single feature selector does not have to be wrapped
            in a list.
            Make sure to also set *share_selected_features*.

        predictors (Union[:class:`~getml.predictors._Predictor`, List[:class:`~getml.predictors._Predictor`]], optional):
            Predictor(s) used to generate the predictions.
            If more than one predictor is passed, the predictions
            generated will be averaged.
            Must be from :mod:`~getml.predictors`.
            A single predictor does not have to be wrapped
            in a list.

        loss_function (str or None):
            The loss function to use for the feature learners.

        tags (List[str], optional): Tags exist to help you organize your pipelines.
            You can add any tags that help you remember what you were
            trying to do.

        include_categorical (bool, optional):
            Whether you want to pass categorical columns
            in the population table to the predictor.

        share_selected_features(float, optional):
            The share of features you want the feature
            selection to keep. When set to 0.0, then all features will be kept.

    Examples:
        We assume that you have already set up your
        preprocessors (refer to :mod:`~getml.preprocessors`),
        your feature learners (refer to :mod:`~getml.feature_learning`)
        as well as your feature selectors and predictors
        (refer to :mod:`~getml.predictors`, which can be used
        for prediction and feature selection).

        You might also want to refer to
        :class:`~getml.DataFrame`, :class:`~getml.data.View`,
        :class:`~getml.data.DataModel`, :class:`~getml.data.Container`,
        :class:`~getml.data.Placeholder` and
        :class:`~getml.data.StarSchema`.

        If you want to create features for a time series problem,
        the easiest way to do so is to use the :class:`~getml.data.TimeSeries`
        abstraction.

        Note that this example is taken from the
        `robot notebook <https://nbviewer.getml.com/github/getml/getml-demo/blob/master/robot.ipynb>`_.

        .. code-block:: python

            # All rows before row 10500 will be used for training.
            split = getml.data.split.time(data_all, "rowid", test=10500)

            time_series = getml.data.TimeSeries(
                population=data_all,
                time_stamps="rowid",
                split=split,
                lagged_targets=False,
                memory=30,
            )

            pipe = getml.Pipeline(
                data_model=time_series.data_model,
                feature_learners=[...],
                predictors=...
            )

            pipe.check(time_series.train)

            pipe.fit(time_series.train)

            pipe.score(time_series.test)

            # To generate predictions on new data,
            # it is sufficient to use a Container.
            # You don't have to recreate the entire
            # TimeSeries, because the abstract data model
            # is stored in the pipeline.
            container = getml.data.Container(
                population=population_new,
            )

            # Add the data as a peripheral table, for the
            # self-join.
            container.add(population=population_new)

            predictions = pipe.predict(container.full)

        If your data can be organized in a simple star schema,
        you can use :class:`~getml.data.StarSchema`.
        :class:`~getml.data.StarSchema` unifies
        :class:`~getml.data.Container` and :class:`~getml.data.DataModel`:

        Note that this example is taken from the
        `loans notebook <https://nbviewer.getml.com/github/getml/getml-demo/blob/master/loans.ipynb>`_.

        .. code-block:: python

            # First, we insert our data into a StarSchema.
            # population_train and population_test are either
            # DataFrames or Views. The population table
            # defines the statistical population of your
            # machine learning problem and contains the
            # target variables.
            star_schema = getml.data.StarSchema(
                train=population_train,
                test=population_test
            )

            # meta, order and trans are either
            # DataFrames or Views.
            # Because this is a star schema,
            # all joins take place on the population
            # table.
            star_schema.join(
                trans,
                on="account_id",
                time_stamps=("date_loan", "date")
            )

            star_schema.join(
                order,
                on="account_id",
            )

            star_schema.join(
                meta,
                on="account_id",
            )

            # Now you can insert your data model,
            # your preprocessors, feature learners,
            # feature selectors and predictors
            # into the pipeline.
            # Note that the pipeline only knows
            # the abstract data model, but hasn't
            # seen the actual data yet.
            pipe = getml.Pipeline(
                data_model=star_schema.data_model,
                preprocessors=[mapping],
                feature_learners=[fast_prop],
                feature_selectors=[feature_selector],
                predictors=predictor,
            )

            # Now, we pass the actual data.
            # This passes 'population_train' and the
            # peripheral tables (meta, order and trans)
            # to the pipeline.
            pipe.check(star_schema.train)

            pipe.fit(star_schema.train)

            pipe.score(star_schema.test)

        :class:`~getml.data.StarSchema` is simpler,
        but cannot be used for more complex data models.
        The general approach is to use
        :class:`~getml.data.Container` and :class:`~getml.data.DataModel`:

        .. code-block:: python

            # First, we insert our data into a Container.
            # population_train and population_test are either
            # DataFrames or Views.
            container = getml.data.Container(
                train=population_train,
                test=population_test
            )

            # meta, order and trans are either
            # DataFrames or Views. They are given
            # aliases, so we can refer to them in the
            # DataModel.
            container.add(
                meta=meta,
                order=order,
                trans=trans
            )

            # Freezing makes the container immutable.
            # This is not required, but often a good idea.
            container.freeze()

            # The abstract data model is constructed
            # using the DataModel class. A data model
            # does not contain any actual data. It just
            # defines the abstract relational structure.
            dm = getml.data.DataModel(
                population_train.to_placeholder("population")
            )

            dm.add(getml.data.to_placeholder(
                meta=meta,
                order=order,
                trans=trans)
            )

            dm.population.join(
                dm.trans,
                on="account_id",
                time_stamps=("date_loan", "date")
            )

            dm.population.join(
                dm.order,
                on="account_id",
            )

            dm.population.join(
                dm.meta,
                on="account_id",
            )

            # Now you can insert your data model,
            # your preprocessors, feature learners,
            # feature selectors and predictors
            # into the pipeline.
            # Note that the pipeline only knows
            # the abstract data model, but hasn't
            # seen the actual data yet.
            pipe = getml.Pipeline(
                data_model=dm,
                preprocessors=[mapping],
                feature_learners=[fast_prop],
                feature_selectors=[feature_selector],
                predictors=predictor,
            )

            # This passes 'population_train' and the
            # peripheral tables (meta, order and trans)
            # to the pipeline.
            pipe.check(container.train)

            pipe.fit(container.train)

            pipe.score(container.test)

        Technically, you don't actually have to use a
        :class:`~getml.data.Container`. You might as well do this
        (in fact, a :class:`~getml.data.Container` is just
        syntactic sugar for this approach):

        .. code-block:: python

            pipe.check(
                population_train,
                {"meta": meta, "order": order, "trans": trans},
            )

            pipe.fit(
                population_train,
                {"meta": meta, "order": order, "trans": trans},
            )

            pipe.score(
                population_test,
                {"meta": meta, "order": order, "trans": trans},
            )

        Or you could even do this. The order of the peripheral tables
        can be inferred from the __repr__ method of the pipeline,
        and it is usually in alphabetical order.

        .. code-block:: python

            pipe.check(
                population_train,
                [meta, order, trans],
            )

            pipe.fit(
                population_train,
                [meta, order, trans],
            )

            pipe.score(
                population_test,
                [meta, order, trans],
            )
    """

    # ------------------------------------------------------------

    def __init__(
        self,
        data_model=None,
        peripheral=None,
        preprocessors=None,
        feature_learners=None,
        feature_selectors=None,
        predictors=None,
        loss_function=None,
        tags=None,
        include_categorical=False,
        share_selected_features=0.5,
    ):

        # ------------------------------------------------------------

        data_model = data_model or DataModel("population")

        # ------------------------------------------------------------

        if not isinstance(data_model, DataModel):
            raise TypeError("'data_model' must be a getml.data.DataModel.")

        # ------------------------------------------------------------

        peripheral = peripheral or _infer_peripheral(data_model.population)

        preprocessors = preprocessors or []

        feature_learners = feature_learners or []

        feature_selectors = feature_selectors or []

        predictors = predictors or []

        tags = tags or []

        # ------------------------------------------------------------

        if not isinstance(preprocessors, list):
            preprocessors = [preprocessors]

        if not isinstance(feature_learners, list):
            feature_learners = [feature_learners]

        if not isinstance(feature_selectors, list):
            feature_selectors = [feature_selectors]

        if not isinstance(predictors, list):
            predictors = [predictors]

        if not isinstance(peripheral, list):
            peripheral = [peripheral]

        if not isinstance(tags, list):
            tags = [tags]

        # ------------------------------------------------------------

        self._id = NOT_FITTED

        self.type = "Pipeline"

        # ------------------------------------------------------------

        feature_learners = [
            _handle_loss_function(fl, loss_function) for fl in feature_learners
        ]

        # ------------------------------------------------------------

        self.data_model = data_model
        self.feature_learners = feature_learners
        self.feature_selectors = feature_selectors
        self.include_categorical = include_categorical
        self.loss_function = loss_function
        self.peripheral = peripheral
        self.predictors = predictors
        self.preprocessors = preprocessors
        self.share_selected_features = share_selected_features
        self.tags = Tags(tags) or Tags([])

        # ------------------------------------------------------------

        self._scores = None

        self._targets = None

        # ------------------------------------------------------------

        Pipeline._supported_params = list(self.__dict__.keys())

        # ------------------------------------------------------------

        self._validate()

    # ----------------------------------------------------------------

    def __eq__(self, other):
        # ------------------------------------------------------------

        if not isinstance(other, Pipeline):
            raise TypeError("A Pipeline can only be compared to another Pipeline")

        # ------------------------------------------------------------

        if len(set(self.__dict__.keys())) != len(set(other.__dict__.keys())):
            return False

        # ------------------------------------------------------------

        for kkey in self.__dict__:

            if kkey not in other.__dict__:
                return False

            # Take special care when comparing numbers.
            if isinstance(self.__dict__[kkey], numbers.Real):
                if not np.isclose(self.__dict__[kkey], other.__dict__[kkey]):
                    return False

            elif self.__dict__[kkey] != other.__dict__[kkey]:
                return False

        # ------------------------------------------------------------

        return True

    # ----------------------------------------------------------------

    def __repr__(self):
        obj_dict = self._make_object_dict()

        sig = _SignatureFormatter(data=obj_dict)
        repr_str = sig._format()

        if self.fitted:
            repr_str += "\n\nurl: " + self._make_url()

        return repr_str

    # ----------------------------------------------------------------

    def _repr_html_(self):
        obj_dict = self._make_object_dict()

        sig = _SignatureFormatter(data=obj_dict)
        repr_str = sig._format()
        html = f"<pre>{repr_str}</pre>"

        if self.fitted:
            url = self._make_url()
            html += (
                "<br><pre>"
                + "url: <a href='"
                + url
                + '\' target="_blank">'
                + url
                + "</a>"
                + "</pre>"
            )

        return html

    # ------------------------------------------------------------

    def _check_classification_or_regression(self):
        """
        Checks whether there are inconsistencies in the algorithms used
        (mixing classification and regression algorithms).
        """

        # -----------------------------------------------------------

        all_classifiers = all(
            [
                elem.loss_function in _classification_loss
                for elem in self.feature_learners
            ]
        )

        all_classifiers = all_classifiers and all(
            [elem.type in _classification_types for elem in self.feature_selectors]
        )

        all_classifiers = all_classifiers and all(
            [elem.type in _classification_types for elem in self.predictors]
        )

        # -----------------------------------------------------------

        all_regressors = all(
            [
                elem.loss_function not in _classification_loss
                for elem in self.feature_learners
            ]
        )

        all_regressors = all_regressors and all(
            [elem.type not in _classification_types for elem in self.feature_selectors]
        )

        all_regressors = all_regressors and all(
            [elem.type not in _classification_types for elem in self.predictors]
        )

        # -----------------------------------------------------------

        if not all_classifiers and not all_regressors:
            raise ValueError(
                """You are mixing classification and regression
                                algorithms. Please make sure that your feature learning
                                algorithms consistently have classification loss functions
                                (like CrossEntropyLoss) or consistently have regression
                                loss functions (like SquareLoss). Also make sure that your
                                feature selectors and predictors are consistently classifiers
                                (like XGBoostClassifier or LogisticRegression) or consistently
                                regressors (like XGBoostRegressor or LinearRegression).
                             """
            )

        # -----------------------------------------------------------

        return all_classifiers

    # ------------------------------------------------------------

    def _check_whether_fitted(self):
        if not self.fitted:
            raise ValueError("Pipeline has not been fitted!")

    # ------------------------------------------------------------

    def _close(self, sock):
        if not isinstance(sock, socket.socket):
            raise TypeError("'sock' must be a socket.")

        # ------------------------------------------------------------

        cmd = dict()
        cmd["type_"] = self.type + ".close"
        cmd["name_"] = self.id

        comm.send_string(sock, json.dumps(cmd))

        msg = comm.recv_string(sock)

        if msg != "Success!":
            comm.engine_exception_handler(msg)

    # ------------------------------------------------------------

    def _get_latest_score(self, score):
        nan_ = [np.nan] * len(self.targets)

        if score not in _all_metrics:
            raise AttributeError(f"Not a valid score name: {score}")

        if not self.scored:
            return nan_

        if self.is_classification and score not in _classification_metrics:
            return nan_

        if self.is_regression and score in _classification_metrics:
            return nan_

        return self._scores[score]

    # ------------------------------------------------------------

    def _getml_deserialize(self):
        """
        Expresses the pipeline in a form the engine can understand.
        """

        cmd = dict()

        self_dict = self.__dict__

        cmd["name_"] = self.id

        for key, value in self_dict.items():
            cmd[key + "_"] = value

        del cmd["_id_"]
        del cmd["_scores_"]
        del cmd["_targets_"]

        return cmd

    # ----------------------------------------------------------------

    def _make_object_dict(self):
        obj_dict = copy.deepcopy(self.__dict__)

        obj_dict["data_model"] = self.data_model.population.name

        obj_dict["peripheral"] = [elem.name for elem in self.peripheral]

        obj_dict["preprocessors"] = [elem.type for elem in self.preprocessors]

        obj_dict["feature_learners"] = [elem.type for elem in self.feature_learners]

        obj_dict["feature_selectors"] = [elem.type for elem in self.feature_selectors]

        obj_dict["predictors"] = [elem.type for elem in self.predictors]

        return obj_dict

    # ----------------------------------------------------------------

    def _make_score_history(self):

        # ------------------------------------------------------------

        scores = self._scores["history"]
        scores = [_replace_with_nan_maybe(score) for score in scores]

        # ------------------------------------------------------------

        if self.is_classification:
            return [
                ClassificationScore(
                    date_time=datetime.strptime(
                        score.get("date_time"), "%Y-%m-%d %H:%M:%S"
                    ),
                    set_used=score.get("set_used"),
                    target=target,
                    accuracy=score.get(accuracy)[target_num],
                    auc=score.get(auc)[target_num],
                    cross_entropy=score.get(cross_entropy)[target_num],
                )
                for score in scores
                for target_num, target in enumerate(self.targets)
            ]

        # ------------------------------------------------------------

        return [
            RegressionScore(
                date_time=datetime.strptime(
                    score.get("date_time"), "%Y-%m-%d %H:%M:%S"
                ),
                set_used=score.get("set_used"),
                target=target,
                mae=score.get(mae)[target_num],
                rmse=score.get(rmse)[target_num],
                rsquared=score.get(rsquared)[target_num],
            )
            for score in scores
            for target_num, target in enumerate(self.targets)
        ]

    # ----------------------------------------------------------------

    def _make_url(self):
        url = comm._monitor_url()
        url += "getpipeline/" + comm._get_project_name() + "/" + self.id + "/0/"
        return url

    # ----------------------------------------------------------------

    def _parse_cmd(self, json_obj):

        ptype = json_obj["type_"]

        del json_obj["type_"]

        if ptype != "Pipeline":
            raise ValueError("Expected type 'Pipeline', got '" + ptype + "'.")

        # ------------------------------------------------------------

        preprocessors = [
            _parse_preprocessor(elem) for elem in json_obj["preprocessors_"]
        ]

        del json_obj["preprocessors_"]

        # ------------------------------------------------------------

        feature_learners = [_parse_fe(elem) for elem in json_obj["feature_learners_"]]

        del json_obj["feature_learners_"]

        # ------------------------------------------------------------

        feature_selectors = [
            _parse_pred(elem) for elem in json_obj["feature_selectors_"]
        ]

        del json_obj["feature_selectors_"]

        # ------------------------------------------------------------

        predictors = [_parse_pred(elem) for elem in json_obj["predictors_"]]

        del json_obj["predictors_"]

        # ------------------------------------------------------------

        data_model = _decode_data_model(json_obj["data_model_"])

        del json_obj["data_model_"]

        # ------------------------------------------------------------

        peripheral = [_decode_placeholder(elem) for elem in json_obj["peripheral_"]]

        del json_obj["peripheral_"]

        # ------------------------------------------------------------

        id_ = json_obj["name_"]

        del json_obj["name_"]

        # ------------------------------------------------------------

        kwargs = _remove_trailing_underscores(json_obj)

        self.__init__(
            data_model=data_model,
            peripheral=peripheral,
            preprocessors=preprocessors,
            feature_learners=feature_learners,
            feature_selectors=feature_selectors,
            predictors=predictors,
            **kwargs,
        )

        self._id = id_

        # ------------------------------------------------------------

        return self

    # ----------------------------------------------------------------

    def _parse_json_obj(self, all_json_objs):

        # ------------------------------------------------------------

        obj = all_json_objs["obj"]

        scores = all_json_objs["scores"]

        targets = all_json_objs["targets"]

        # ------------------------------------------------------------

        self._parse_cmd(obj)

        # ------------------------------------------------------------

        scores = _remove_trailing_underscores(scores)
        scores = _replace_with_nan_maybe(scores)

        self._scores = scores

        self._targets = targets

        # ------------------------------------------------------------

        return self

    # ----------------------------------------------------------------

    def _save(self):
        """
        Saves the pipeline as a JSON file.
        """

        # ------------------------------------------------------------

        cmd = dict()
        cmd["type_"] = self.type + ".save"
        cmd["name_"] = self.id

        comm.send(cmd)

    # ------------------------------------------------------------

    def _send(self, additional_tags=None):

        # ------------------------------------------------------------

        self._validate()

        # ------------------------------------------------------------

        self._id = _make_id()

        cmd = self._getml_deserialize()

        if additional_tags is not None:
            cmd["tags_"] += additional_tags

        comm.send(cmd)

        # ------------------------------------------------------------

        return self

    # ------------------------------------------------------------

    def _transform(
        self,
        peripheral_data_frames,
        population_data_frame,
        sock,
        score=False,
        predict=False,
        df_name="",
        table_name="",
    ):
        # ------------------------------------------------------------

        _check_df_types(population_data_frame, peripheral_data_frames)

        if not isinstance(sock, socket.socket):
            raise TypeError("'sock' must be a socket.")

        if not isinstance(score, bool):
            raise TypeError("'score' must be of type bool")

        if not isinstance(predict, bool):
            raise TypeError("'predict' must be of type bool")

        if not isinstance(table_name, str):
            raise TypeError("'table_name' must be of type str")

        if not isinstance(df_name, str):
            raise TypeError("'df_name' must be of type str")

        # ------------------------------------------------------------

        cmd = dict()
        cmd["type_"] = self.type + ".transform"
        cmd["name_"] = self.id

        cmd["score_"] = score
        cmd["predict_"] = predict

        cmd["peripheral_dfs_"] = [
            df._getml_deserialize() for df in peripheral_data_frames
        ]
        cmd["population_df_"] = population_data_frame._getml_deserialize()

        cmd["df_name_"] = df_name
        cmd["table_name_"] = table_name

        comm.send_string(sock, json.dumps(cmd))

        # ------------------------------------------------------------
        # Do the actual transformation

        msg = comm.log(sock)

        if msg == "Success!":
            if table_name == "" and df_name == "" and not score:
                yhat = comm.recv_float_matrix(sock)
            else:
                yhat = None
        else:
            comm.engine_exception_handler(msg)

        print()

        # ------------------------------------------------------------

        return yhat

    # ----------------------------------------------------------------

    @property
    def accuracy(self):
        """
        A convenience wrapper to retrieve the accuracy of the latest scoring run (the
        last time `.score()` was called) on the pipeline.

        For programmatic access use `~getml.pipeline.metrics`.
        """
        return self.scores.accuracy

    # ----------------------------------------------------------------

    @property
    def auc(self):
        """
        A convenience wrapper to retrieve the auc of the latest scoring run (the
        last time `.score()` was called) on the pipeline.

        For programmatic access use `~getml.pipeline.metrics`.
        """
        return self.scores.auc

    # ----------------------------------------------------------------

    def check(self, population_table, peripheral_tables=None):
        """
        Checks the validity of the data model.

        Args:
            population_table (:class:`~getml.DataFrame`, :class:`~getml.data.View` or :class:`~getml.data.Subset`):
                Main table containing the target variable(s) and
                corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable.

            peripheral_tables (List[:class:`~getml.DataFrame` or :class:`~getml.data.View`], dict, :class:`~getml.DataFrame` or :class:`~getml.data.View`, optional):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. If passed as a list, the order needs to
                match the order of the corresponding placeholders passed
                to ``peripheral``.

                If you pass a :class:`~getml.data.Subset` to `population_table`,
                the peripheral tables from that subset will be used. If you use
                a :class:`~getml.data.Container`, :class:`~getml.data.StarSchema`
                or :class:`~getml.data.TimeSeries`, that means you are passing
                a :class:`~getml.data.Subset`.

        """

        # ------------------------------------------------------------

        if isinstance(population_table, data.Subset):
            peripheral_tables = population_table.peripheral
            population_table = population_table.population

        # ------------------------------------------------------------

        peripheral_tables = _transform_peripheral(peripheral_tables, self.peripheral)

        _check_df_types(population_table, peripheral_tables)

        # ------------------------------------------------------------

        temp = copy.deepcopy(self)

        # ------------------------------------------------------------

        temp._send()

        # ------------------------------------------------------------

        cmd = dict()

        cmd["type_"] = temp.type + ".check"
        cmd["name_"] = temp.id

        cmd["peripheral_dfs_"] = [df._getml_deserialize() for df in peripheral_tables]
        cmd["population_df_"] = population_table._getml_deserialize()

        # ------------------------------------------------------------

        sock = comm.send_and_get_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Found!":
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        print("Checking data model...")

        msg = comm.log(sock)

        if msg != "Success!":
            comm.engine_exception_handler(msg)

        print()

        no_warnings = comm.recv_warnings(sock)

        if no_warnings:
            print("OK.")

        # ------------------------------------------------------------

        sock.close()

        # ------------------------------------------------------------

        temp.delete()

    # ------------------------------------------------------------

    @property
    def columns(self):
        """
        :class:`~getml.pipeline.Columns` object that
        can be used to handle the columns generated
        by the feature learners.
        """
        self._check_whether_fitted()
        return Columns(self.id, self.targets, self.peripheral)

    # ----------------------------------------------------------------

    @property
    def cross_entropy(self):
        """
        A convenience wrapper to retrieve the cross entropy of the latest scoring
        run (the last time `.score()` was called) on the pipeline.

        For programmatic access use `~getml.pipeline.metrics`.
        """
        return self.scores.cross_entropy

    # ----------------------------------------------------------------

    def delete(self):
        """
        Deletes the pipeline from the engine.

        Note:
            Caution: You can not undo this action!
        """
        self._check_whether_fitted()

        cmd = dict()
        cmd["type_"] = self.type + ".delete"
        cmd["name_"] = self.id
        cmd["mem_only_"] = False

        comm.send(cmd)

        self._id = NOT_FITTED

    # ------------------------------------------------------------

    def deploy(self, deploy):
        """Allows a fitted pipeline to be addressable via an HTTP request.
        See :ref:`deployment` for details.

        Args:
            deploy (bool): If :code:`True`, the deployment of the pipeline
                will be triggered.
        """

        # ------------------------------------------------------------

        self._check_whether_fitted()

        # ------------------------------------------------------------

        if not isinstance(deploy, bool):
            raise TypeError("'deploy' must be of type bool")

        # ------------------------------------------------------------

        self._validate()

        # ------------------------------------------------------------

        cmd = dict()
        cmd["type_"] = self.type + ".deploy"
        cmd["name_"] = self.id
        cmd["deploy_"] = deploy

        comm.send(cmd)

        self._save()

    # ------------------------------------------------------------

    @property
    def features(self):
        """
        :class:`~getml.pipeline.Features` object that
        can be used to handle the features generated
        by the feature learners.
        """
        self._check_whether_fitted()
        return Features(self.id, self.targets)

    # ------------------------------------------------------------

    def fit(self, population_table, peripheral_tables=None, validation_table=None):
        """Trains the feature learning algorithms, feature selectors
        and predictors.

        Args:
            population_table (:class:`~getml.DataFrame`, :class:`~getml.data.View` or :class:`~getml.data.Subset`):
                Main table containing the target variable(s) and
                corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable.

            peripheral_tables (List[:class:`~getml.DataFrame` or :class:`~getml.data.View`], dict, :class:`~getml.DataFrame` or :class:`~getml.data.View`, optional):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. If passed as a list, the order needs to
                match the order of the corresponding placeholders passed
                to ``peripheral``.

                If you pass a :class:`~getml.data.Subset` to `population_table`,
                the peripheral tables from that subset will be used. If you use
                a :class:`~getml.data.Container`, :class:`~getml.data.StarSchema`
                or :class:`~getml.data.TimeSeries`, that means you are passing
                a :class:`~getml.data.Subset`.

            validation_table (:class:`~getml.DataFrame`, :class:`~getml.data.View` or :class:`~getml.data.Subset`):
                Main table containing the target variable(s) and
                corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable. If you are passing a subset, that subset
                must be derived from the same container as *population_table*.

                Only used for early stopping in :class:`~getml.predictors.XGBoostClassifier`
                and :class:`~getml.predictors.XGBoostRegressor`.
        """

        # ------------------------------------------------------------

        additional_tags = (
            ["container-" + population_table.container_id]
            if isinstance(population_table, data.Subset)
            else []
        )

        if (
            isinstance(population_table, data.Subset)
            and isinstance(validation_table, data.Subset)
            and validation_table.container_id != population_table.container_id
        ):
            raise ValueError(
                "The subset used for validation must be from the same container "
                + "as the subset used for training."
            )

        if isinstance(population_table, data.Subset):
            peripheral_tables = population_table.peripheral
            population_table = population_table.population

        if isinstance(validation_table, data.Subset):
            validation_table = validation_table.population

        # ------------------------------------------------------------

        peripheral_tables = _transform_peripheral(peripheral_tables, self.peripheral)

        _check_df_types(population_table, peripheral_tables)

        # ------------------------------------------------------------

        self.check(population_table, peripheral_tables)

        # ------------------------------------------------------------

        self._send(additional_tags)

        # ------------------------------------------------------------

        cmd = dict()

        cmd["type_"] = self.type + ".fit"
        cmd["name_"] = self.id

        cmd["peripheral_dfs_"] = [df._getml_deserialize() for df in peripheral_tables]
        cmd["population_df_"] = population_table._getml_deserialize()

        if validation_table is not None:
            cmd["validation_df_"] = validation_table._getml_deserialize()

        # ------------------------------------------------------------

        sock = comm.send_and_get_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Found!":
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        begin = time.time()

        msg = comm.log(sock)

        end = time.time()

        # ------------------------------------------------------------

        if "Trained" in msg:
            print()
            print(msg)
            _print_time_taken(begin, end, "Time taken: ")
        else:
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        sock.close()

        # ------------------------------------------------------------

        self._save()

        # ------------------------------------------------------------

        return self.refresh()

    # ------------------------------------------------------------

    @property
    def fitted(self):
        """
        Whether the pipeline has already been fitted.
        """
        return self._id != NOT_FITTED

    # ----------------------------------------------------------------

    @property
    def mae(self):
        """
        A convenience wrapper to retrieve the mae of the latest scoring run (the
        last time `.score()` was called) on the pipeline.

        For programmatic access use `~getml.pipeline.metrics`.
        """
        return self.scores.mae

    # ------------------------------------------------------------

    @property
    def plots(self):
        """
        :class:`~getml.pipeline.Plots` object that
        can be used to generate plots like an ROC
        curve or a lift curve.
        """
        self._check_whether_fitted()
        return Plots(self.id)

    # ------------------------------------------------------------

    @property
    def id(self):
        """
        ID of the pipeline. This is used to uniquely identify
        the pipeline on the engine.
        """
        return self._id

    # ------------------------------------------------------------

    @property
    def is_classification(self):
        """
        Whether the pipeline can used for classification problems.
        """
        return self._check_classification_or_regression()

    # ------------------------------------------------------------

    @property
    def is_regression(self):
        """
        Whether the pipeline can used for regression problems.
        """
        return not self.is_classification

    # ------------------------------------------------------------

    @property
    def name(self):
        """
        Returns the ID of the pipeline. The name property is
        kept for backward compatibility.
        """
        return self._id

    # ------------------------------------------------------------

    def predict(self, population_table, peripheral_tables=None, table_name=""):
        """Forecasts on new, unseen data using the trained ``predictor``.

        Returns the predictions generated by the pipeline based on
        `population_table` and `peripheral_tables` or writes them into
        a data base named `table_name`.

        Args:
            population_table (:class:`~getml.DataFrame`, :class:`~getml.data.View` or :class:`~getml.data.Subset`):
                Main table containing the target variable(s) and
                corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable.

            peripheral_tables (List[:class:`~getml.DataFrame` or :class:`~getml.data.View`], dict, :class:`~getml.DataFrame` or :class:`~getml.data.View`, optional):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. If passed as a list, the order needs to
                match the order of the corresponding placeholders passed
                to ``peripheral``.

                If you pass a :class:`~getml.data.Subset` to `population_table`,
                the peripheral tables from that subset will be used. If you use
                a :class:`~getml.data.Container`, :class:`~getml.data.StarSchema`
                or :class:`~getml.data.TimeSeries`, that means you are passing
                a :class:`~getml.data.Subset`.

            table_name (str, optional):
                If not an empty string, the resulting predictions will
                be written into a table in a :mod:`~getml.database`.
                Refer to :ref:`unified_import_interface` for further information.

        Return:
            :class:`numpy.ndarray`:
                Resulting predictions provided in an array of the
                (number of rows in `population_table`, number of
                targets in `population_table`).

        Note:
            Only fitted pipelines
            (:meth:`~getml.Pipeline.fit`) can be used for
            prediction.

        """

        # ------------------------------------------------------------

        self._check_whether_fitted()

        # ------------------------------------------------------------

        if isinstance(population_table, data.Subset):
            peripheral_tables = population_table.peripheral
            population_table = population_table.population

        # ------------------------------------------------------------

        peripheral_tables = _transform_peripheral(peripheral_tables, self.peripheral)

        _check_df_types(population_table, peripheral_tables)

        if not isinstance(table_name, str):
            raise TypeError("'table_name' must be of type str")

        # ------------------------------------------------------------

        self._validate()

        # ------------------------------------------------------------

        # Prepare the command for the getML engine.
        cmd = dict()
        cmd["type_"] = self.type + ".transform"
        cmd["name_"] = self.id
        cmd["http_request_"] = False

        # ------------------------------------------------------------

        # Send command to engine and make sure that pipeline has
        # been found.
        sock = comm.send_and_get_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Found!":
            sock.close()
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        y_hat = self._transform(
            peripheral_tables,
            population_table,
            sock,
            predict=True,
            table_name=table_name,
        )

        # ------------------------------------------------------------

        # Close the connection to the engine.
        sock.close()

        # ------------------------------------------------------------

        return y_hat

    # ------------------------------------------------------------

    def refresh(self):
        """Reloads the pipeline from the engine.

        This discards all local changes you have made since the
        last time you called :meth:`~getml.Pipeline.fit`.

        Returns:
            :class:`~getml.Pipeline`:
                Current instance
        """

        # ------------------------------------------------------------

        cmd = dict()
        cmd["type_"] = self.type + ".refresh"
        cmd["name_"] = self.id

        sock = comm.send_and_get_socket(cmd)

        # ------------------------------------------------------------

        msg = comm.recv_string(sock)

        sock.close()

        if msg[0] != "{":
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        json_obj = json.loads(msg)

        self._parse_json_obj(json_obj)

        # ------------------------------------------------------------

        return self

    # ----------------------------------------------------------------

    @property
    def rmse(self):
        """
        A convenience wrapper to retrieve the rmse of the latest scoring run
        (the last time `.score()` was called) on the pipeline.

        For programmatic access use `~getml.pipeline.metrics`.
        """
        return self.scores.rmse

    # ----------------------------------------------------------------

    @property
    def rsquared(self):
        """
        A convenience wrapper to retrieve the rsquared of the latest scoring run
        (the last time `.score()` was called) on the pipeline.

        For programmatic access use `~getml.pipeline.metrics`.
        """
        return self.scores.rsquared

    # ----------------------------------------------------------------

    def score(self, population_table, peripheral_tables=None):
        """Calculates the performance of the ``predictor``.

        Returns different scores calculated on `population_table` and
        `peripheral_tables`.

        Args:
            population_table (:class:`~getml.DataFrame`, :class:`~getml.data.View` or :class:`~getml.data.Subset`):
                Main table containing the target variable(s) and
                corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable.

            peripheral_tables (List[:class:`~getml.DataFrame` or :class:`~getml.data.View`], dict, :class:`~getml.DataFrame` or :class:`~getml.data.View`, optional):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. If passed as a list, the order needs to
                match the order of the corresponding placeholders passed
                to ``peripheral``.

                If you pass a :class:`~getml.data.Subset` to `population_table`,
                the peripheral tables from that subset will be used. If you use
                a :class:`~getml.data.Container`, :class:`~getml.data.StarSchema`
                or :class:`~getml.data.TimeSeries`, that means you are passing
                a :class:`~getml.data.Subset`.

        Note:
            Only fitted pipelines
            (:meth:`~getml.Pipeline.fit`) can be
            scored.
        """

        # ------------------------------------------------------------

        self._check_whether_fitted()

        # ------------------------------------------------------------

        if isinstance(population_table, data.Subset):
            peripheral_tables = population_table.peripheral
            population_table = population_table.population

        # ------------------------------------------------------------

        peripheral_tables = _transform_peripheral(peripheral_tables, self.peripheral)

        _check_df_types(population_table, peripheral_tables)

        # ------------------------------------------------------------

        # Prepare the command for the getml engine.
        cmd = dict()
        cmd["type_"] = self.type + ".transform"
        cmd["name_"] = self.id
        cmd["http_request_"] = False

        # ------------------------------------------------------------

        # Send command to engine and make sure that pipeline has
        # been found.
        sock = comm.send_and_get_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Found!":
            sock.close()
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        self._transform(
            peripheral_tables, population_table, sock, predict=True, score=True
        )

        # ------------------------------------------------------------

        msg = comm.recv_string(sock)

        if msg != "Success!":
            sock.close()
            comm.engine_exception_handler(msg)

        scores = comm.recv_string(sock)

        scores = json.loads(scores)

        # ------------------------------------------------------------

        self.refresh()

        self._save()

        # ------------------------------------------------------------

        return self.scores

    # ----------------------------------------------------------------

    @property
    def scores(self):
        """
        Contains all scores generated by :meth:`~getml.Pipeline.score`

        Returns:
            :class:`~getml.pipeline.Scores`:
                A container that holds the scores for the pipeline.

        """
        self._check_whether_fitted()

        scores = self._make_score_history()

        latest = {score: self._get_latest_score(score) for score in _all_metrics}

        return Scores(scores, latest)

    # ----------------------------------------------------------------

    @property
    def scored(self):
        """
        Whether the pipeline has been scored.
        """
        if self._scores is None:
            return False
        return len(self._scores) > 1

    # ----------------------------------------------------------------
    @property
    def targets(self):
        """
        Contains the names of the targets used for this pipeline.
        """
        self._check_whether_fitted()
        return copy.deepcopy(self._targets)

    # ----------------------------------------------------------------

    def transform(
        self, population_table, peripheral_tables=None, df_name="", table_name=""
    ):
        """Translates new data into the trained features.

        Transforms the data passed in `population_table` and
        `peripheral_tables` into features, which can be inserted into
        machine learning models.

        Examples:
             By default, transform returns a :class:`numpy.ndarray`:

             .. code-block:: python

                my_features_array = pipe.transform()

             You can also export your features as a :class:`~getml.DataFrame`
             by providing the `df_name` argument:

             .. code-block:: python

                my_features_df = pipe.transform(df_name="my_features")

             Or you can write the results directly into a database:

             .. code-block:: python

                getml.database.connect_odbc(...)
                pipe.transform(table_name="MY_FEATURES")

        Args:
            population_table (:class:`~getml.DataFrame`, :class:`~getml.data.View` or :class:`~getml.data.Subset`):
                Main table containing the target variable(s) and
                corresponding to the ``population``
                :class:`~getml.data.Placeholder` instance
                variable.

            peripheral_tables (List[:class:`~getml.DataFrame` or :class:`~getml.data.View`], dict, :class:`~getml.DataFrame` or :class:`~getml.data.View`, optional):
                Additional tables corresponding to the ``peripheral``
                :class:`~getml.data.Placeholder` instance
                variable. If passed as a list, the order needs to
                match the order of the corresponding placeholders passed
                to ``peripheral``.

                If you pass a :class:`~getml.data.Subset` to `population_table`,
                the peripheral tables from that subset will be used. If you use
                a :class:`~getml.data.Container`, :class:`~getml.data.StarSchema`
                or :class:`~getml.data.TimeSeries`, that means you are passing
                a :class:`~getml.data.Subset`.

            df_name (str, optional):
                If not an empty string, the resulting features will be
                written into a newly created DataFrame.

            table_name (str, optional):
                If not an empty string, the resulting features will
                be written into a table in a :mod:`~getml.database`.
                Refer to :ref:`unified_import_interface` for further information.

        Note:
            Only fitted pipelines
            (:meth:`~getml.Pipeline.fit`) can transform
            data into features.
        """

        # ------------------------------------------------------------

        self._check_whether_fitted()

        # ------------------------------------------------------------

        if isinstance(population_table, data.Subset):
            peripheral_tables = population_table.peripheral
            population_table = population_table.population

        # ------------------------------------------------------------

        peripheral_tables = _transform_peripheral(peripheral_tables, self.peripheral)

        _check_df_types(population_table, peripheral_tables)

        # ------------------------------------------------------------

        self._validate()

        # ------------------------------------------------------------

        cmd = dict()
        cmd["type_"] = self.type + ".transform"
        cmd["name_"] = self.id
        cmd["http_request_"] = False

        # ------------------------------------------------------------

        sock = comm.send_and_get_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Found!":
            sock.close()
            comm.engine_exception_handler(msg)

        # ------------------------------------------------------------

        y_hat = self._transform(
            peripheral_tables,
            population_table,
            sock,
            df_name=df_name,
            table_name=table_name,
        )

        # ------------------------------------------------------------

        sock.close()

        # ------------------------------------------------------------

        if df_name != "":
            y_hat = data.DataFrame(name=df_name).refresh()

        # ------------------------------------------------------------

        return y_hat

    # ----------------------------------------------------------------

    def _validate(self):

        # ------------------------------------------------------------

        if not isinstance(self.id, str):
            raise TypeError("'name' must be of type str")

        if not isinstance(self.data_model, DataModel):
            raise TypeError("'data_model' must be a getml.data.DataModel.")

        if not _is_typed_list(self.peripheral, data.Placeholder):
            raise TypeError(
                "'peripheral' must be either a getml.data.Placeholder or a list thereof"
            )

        if not _is_subclass_list(self.preprocessors, _Preprocessor):
            raise TypeError("'preprocessor' must be a list of _Preprocessor.")

        if not _is_subclass_list(self.feature_learners, _FeatureLearner):
            raise TypeError("'feature_learners' must be a list of _FeatureLearners.")

        if not _is_subclass_list(self.feature_selectors, _Predictor):
            raise TypeError(
                "'feature_selectors' must be a list of getml.predictors._Predictors."
            )

        if not _is_subclass_list(self.predictors, _Predictor):
            raise TypeError(
                "'predictors' must be a list of getml.predictors._Predictors."
            )

        if not isinstance(self.include_categorical, bool):
            raise TypeError("'include_categorical' must be a bool!")

        if not isinstance(self.share_selected_features, numbers.Real):
            raise TypeError("'share_selected_features' must be number!")

        if not _is_typed_list(self.tags, str):
            raise TypeError("'tags' must be a list of str.")

        # ------------------------------------------------------------

        if self.type != "Pipeline":
            raise ValueError("'type' must be 'Pipeline'")

        # ------------------------------------------------------------

        for kkey in self.__dict__:
            if kkey not in Pipeline._supported_params:
                raise KeyError(
                    """Instance variable ["""
                    + kkey
                    + """]
                       is not supported in Pipeline."""
                )

        # ------------------------------------------------------------

        for elem in self.feature_learners:
            elem.validate()

        for elem in self.feature_selectors:
            elem.validate()

        for elem in self.predictors:
            elem.validate()

        # ------------------------------------------------------------

        self._check_classification_or_regression()

        # ------------------------------------------------------------
