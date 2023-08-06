# Copyright [2020] [Toyota Research Institute]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Module and scripts for generating feature objects from structured
battery cycling data, to be used as inputs for machine learning
early prediction models.

Usage:
    featurize [INPUT_JSON]

Options:
    -h --help        Show this screen
    --version        Show version


The `featurize` script will generate features according to the methods
contained in beep.featurize.  It places output files corresponding to
features in `/data-share/features/`.

The input json must contain the following fields

* `file_list` - a list of processed cycler runs for which to generate features

The output json file will contain the following:

* `file_list` - a list of filenames corresponding to the locations of the features

Example:
```angular2
$ featurize '{"invalid_file_list": ["/data-share/renamed_cycler_files/FastCharge/FastCharge_0_CH33.csv",
    "/data-share/renamed_cycler_files/FastCharge/FastCharge_1_CH44.csv"],
    "file_list": ["/data-share/structure/FastCharge_2_CH29_structure.json"]}'
{"file_list": ["/data-share/features/FastCharge_2_CH29_full_model_features.json"]}
```
"""

import os
import json
import numpy as np
import pandas as pd
from docopt import docopt
from monty.json import MSONable
from monty.serialization import loadfn, dumpfn
from scipy.stats import skew, kurtosis

from beep.structure.cli import auto_load_processed
from beep.utils import WorkflowOutputs
from beep.features import featurizer_helpers, intracell_losses
from beep.features.base import BeepFeatures
from beep import logger, __version__

MODULE_DIR = os.path.dirname(__file__)
FEATURE_HYPERPARAMS = loadfn(
    os.path.join(MODULE_DIR, "features/feature_hyperparameters.yaml")
)

s = {"service": "DataAnalyzer"}


class HPPCResistanceVoltageFeatures(BeepFeatures):
    """
    Object corresponding to resistance, voltage and diffusion related
    features generated from hybrid pulse power characterization cycles.
    Includes constructors to create the features, object names and metadata.

    Attributes:
        name (str): predictor object name.
        X (pandas.DataFrame): features in DataFrame format.
        metadata (dict): information about the conditions, data
            and code used to produce features

    """

    # Class name for the feature object
    class_feature_name = "HPPCResistanceVoltageFeatures"

    def __init__(self, name, X, metadata):
        """
        Args:
            name (str): predictor object name
            X (pandas.DataFrame): features in DataFrame format.
            metadata (dict): information about the data and code used to produce features
        """
        super().__init__(name, X, metadata)
        self.name = name
        self.X = X
        self.metadata = metadata

    @classmethod
    def validate_data(cls, processed_cycler_run, params_dict=None):
        """
        This function determines if the input data has the necessary attributes for
        creation of this feature class. It should test for all of the possible reasons
        that feature generation would fail for this particular input data.

        Args:
            processed_cycler_run (beep.structure.ProcessedCyclerRun): data from cycler run
            params_dict (dict): dictionary of parameters governing how the ProcessedCyclerRun object
            gets featurized. These could be filters for column or row operations

        Returns:
            (bool): True/False indication of ability to proceed with feature generation
        """
        conditions = []
        if not hasattr(processed_cycler_run, "diagnostic_summary") & hasattr(
            processed_cycler_run, "diagnostic_data"
        ):
            return False
        if processed_cycler_run.diagnostic_summary is None:
            return False
        elif processed_cycler_run.diagnostic_summary.empty:
            return False
        else:
            conditions.append(
                any(
                    [
                        "hppc" in x
                        for x in processed_cycler_run.diagnostic_summary.cycle_type.unique()
                    ]
                )
            )

        return all(conditions)

    @classmethod
    def features_from_processed_cycler_run(cls, processed_cycler_run, params_dict=None,
                                           parameters_path="data-share/raw/parameters"):
        """
        This method calculates features based on voltage, diffusion and resistance changes in hppc cycles.

        Note: Inside this function it calls function get_dr_df, but if the cell does not state of charge from 20% to
        10%, the function will fail, and throw you error messages. This will only happen after cycle 37 and on fast
        charging cells. Also, this function calls function get_v_diff, which takes in an argument soc_window, if you
        want more correlation, you should go for low state of charge, which corresponds to soc_window = 8. However,
        like the resistance feature, at cycle 142 and beyond, soc_window = 8 might fail on fast charged cells. For
        lower soc_window values, smaller than or equal to 7, this should not be a problem, but it will not give you
        high correlations.

        Args:
            processed_cycler_run (beep.structure.ProcessedCyclerRun)
            params_dict (dict): dictionary of parameters governing how the ProcessedCyclerRun object
            gets featurized. These could be filters for column or row operations
            parameters_path (str): Root directory storing project parameter files.


        Returns:
            dataframe of features based on voltage and resistance changes over a SOC window in hppc cycles
        """
        if params_dict is None:
            params_dict = FEATURE_HYPERPARAMS[cls.class_feature_name]

        # Filter out low cycle numbers at the end of the test, corresponding to the "final" diagnostic
        processed_cycler_run.diagnostic_data = processed_cycler_run.diagnostic_data[
                ~((processed_cycler_run.diagnostic_data.test_time > params_dict['test_time_filter_sec']) &
                  (processed_cycler_run.diagnostic_data.cycle_index < params_dict['cycle_index_filter']))
            ]
        processed_cycler_run.diagnostic_data = processed_cycler_run.diagnostic_data.groupby(
            ["cycle_index", "step_index", "step_index_counter"]
        ).filter(lambda x: ~x["test_time"].isnull().all())

        # diffusion features
        diffusion_features = featurizer_helpers.get_diffusion_features(
            processed_cycler_run, params_dict["diag_pos"]
        )

        hppc_r = pd.DataFrame()
        # the 9 by 6 dataframe
        df_dr = featurizer_helpers.get_dr_df(
            processed_cycler_run, params_dict["diag_pos"]
        )
        # transform this dataframe to be 1 by 54
        columns = df_dr.columns
        for column in columns:
            for r in range(len(df_dr[column])):
                name = column + str(r)
                hppc_r[name] = [df_dr[column][r]]

        # the variance of ocv features
        hppc_ocv = featurizer_helpers.get_hppc_ocv(
            processed_cycler_run, params_dict["diag_pos"]
        )

        # the v_diff features
        v_diff = featurizer_helpers.get_v_diff(
            processed_cycler_run, params_dict["diag_pos"], params_dict["soc_window"]
        )

        # merge everything together as a final result dataframe
        return pd.concat([hppc_r, hppc_ocv, v_diff, diffusion_features], axis=1)


class CycleSummaryStats(BeepFeatures):
    """
    Object corresponding to summary statistics from
    regular cycles

    name (str): predictor object name.
    X (pandas.DataFrame): features in DataFrame format.
    metadata (dict): information about the conditions, data
        and code used to produce features
    """

    # Class name for the feature object
    class_feature_name = "CycleSummaryStats"

    def __init__(self, name, X, metadata):
        """
        Args:
            name (str): predictor object name
            X (pandas.DataFrame): features in DataFrame format.
            metadata (dict): information about the data and code used to produce features
        """
        super().__init__(name, X, metadata)
        self.name = name
        self.X = X
        self.metadata = metadata

    @classmethod
    def validate_data(cls, processed_cycler_run, params_dict=None):
        """
        This function determines if the input data has the necessary attributes for
        creation of this feature class. It should test for all of the possible reasons
        that feature generation would fail for this particular input data.

        Args:
            processed_cycler_run (beep.structure.ProcessedCyclerRun): data from cycler run
            params_dict (dict): dictionary of parameters governing how the ProcessedCyclerRun object
                gets featurized. These could be filters for column or row operations
        Returns:
            bool: True/False indication of ability to proceed with feature generation
        """
        if params_dict is None:
            params_dict = FEATURE_HYPERPARAMS[cls.class_feature_name]

        # TODO: not sure this is necessary
        # Check for data in each of the selected cycles
        index_1, index_2 = params_dict['cycle_comp_num']
        cycle_1 = processed_cycler_run.structured_data[
            processed_cycler_run.structured_data.cycle_index == index_1]
        cycle_2 = processed_cycler_run.structured_data[
            processed_cycler_run.structured_data.cycle_index == index_2]
        if len(cycle_1) == 0 or len(cycle_2) == 0:
            return False

        # TODO: check whether this is good
        # Check for relevant data
        required_columns = ['charge_capacity',
                            'discharge_capacity',
                            'charge_energy',
                            'discharge_energy',
                            ]
        pcycler_run_columns = processed_cycler_run.structured_data.columns
        if not all([column in pcycler_run_columns for column in required_columns]):
            return False

        return True

    SUMMARY_STATISTIC_NAMES = ["var", "min", "mean", "skew", "kurtosis", "abs", "square"]

    @staticmethod
    def get_summary_statistics(array):
        """
        Static method for getting values corresponding
        to standard 7 operations that many beep features
        use, i.e. log of absolute value of each of
        variance, min, mean, skew, kurtosis, the sum of
        the absolute values and the sum of squares

        Args:
            array (list, np.ndarray): array of values to get
                standard operation values for, e.g. cycle
                discharging capacity, QcDiff, etc.

        Returns:
            [float]: list of features

        """
        return np.array([
            np.log10(np.absolute(np.var(array))),
            np.log10(np.absolute(min(array))),
            np.log10(np.absolute(np.mean(array))),
            np.log10(np.absolute(skew(array))),
            np.log10(np.absolute(kurtosis(array, fisher=False, bias=False))),
            np.log10(np.sum(np.absolute(array))),
            np.log10(np.sum(np.square(array)))
        ])

    @classmethod
    def features_from_processed_cycler_run(cls, processed_cycler_run, params_dict=None,
                                           parameters_path="data-share/raw/parameters"):
        """
        Generate features listed in early prediction manuscript using both diagnostic and regular cycles

        Args:
            processed_cycler_run (beep.structure.ProcessedCyclerRun)
            params_dict (dict): dictionary of parameters governing how the ProcessedCyclerRun object
                gets featurized. These could be filters for column or row operations
            parameters_path (str): Root directory storing project parameter files.

        Returns:
            X (pd.DataFrame): Dataframe containing the feature
        """
        if params_dict is None:
            params_dict = FEATURE_HYPERPARAMS[cls.class_feature_name]

        # TODO: extend this dataframe and uncomment energy features when
        #   structuring is refactored
        X = pd.DataFrame(np.zeros((1, 28)))

        reg_cycle_comp_num = params_dict.get("cycle_comp_num")
        cycle_comp_1 = processed_cycler_run.structured_data[
            processed_cycler_run.structured_data.cycle_index == reg_cycle_comp_num[1]
            ]
        cycle_comp_0 = processed_cycler_run.structured_data[
            processed_cycler_run.structured_data.cycle_index == reg_cycle_comp_num[0]
            ]
        Qc100_1 = cycle_comp_1[cycle_comp_1.step_type == "charge"].charge_capacity
        Qc10_1 = cycle_comp_0[cycle_comp_0.step_type == "charge"].charge_capacity
        QcDiff = Qc100_1.values - Qc10_1.values
        QcDiff = QcDiff[~np.isnan(QcDiff)]

        X.loc[0, 0:6] = cls.get_summary_statistics(QcDiff)

        Qd100_1 = cycle_comp_1[cycle_comp_1.step_type == "discharge"].discharge_capacity
        Qd10_1 = cycle_comp_0[cycle_comp_0.step_type == "discharge"].discharge_capacity
        QdDiff = Qd100_1.values - Qd10_1.values
        QdDiff = QdDiff[~np.isnan(QdDiff)]

        X.loc[0, 7:13] = cls.get_summary_statistics(QdDiff)

        # # Charging Energy features
        Ec100_1 = cycle_comp_1[cycle_comp_1.step_type == "charge"].charge_energy
        Ec10_1 = cycle_comp_0[cycle_comp_0.step_type == "charge"].charge_energy
        EcDiff = Ec100_1.values - Ec10_1.values
        EcDiff = EcDiff[~np.isnan(EcDiff)]

        X.loc[0, 14:20] = cls.get_summary_statistics(EcDiff)

        # # Discharging Energy features
        Ed100_1 = cycle_comp_1[cycle_comp_1.step_type == "charge"].discharge_energy
        Ed10_1 = cycle_comp_0[cycle_comp_0.step_type == "charge"].discharge_energy
        EdDiff = Ed100_1.values - Ed10_1.values
        EdDiff = EdDiff[~np.isnan(EdDiff)]

        X.loc[0, 21:27] = cls.get_summary_statistics(EdDiff)

        quantities = [
            "charging_capacity",
            "discharging_capacity",
            "charging_energy",
            "discharging_energy",
        ]

        X.columns = [y + "_" + x for x in quantities for y in cls.SUMMARY_STATISTIC_NAMES]

        return X


class DiagnosticSummaryStats(CycleSummaryStats):
    """
    Object corresponding to summary statistics from a diagnostic cycle of
    specific type. Includes constructors to create the features, object names
    and metadata attributes in the object.  Inherits from RegularCycleSummaryStats
    to reuse standard feature generation

    name (str): predictor object name.
    X (pandas.DataFrame): features in DataFrame format.
    metadata (dict): information about the conditions, data
        and code used to produce features
    """

    # Class name for the feature object
    class_feature_name = "DiagnosticSummaryStats"

    def __init__(self, name, X, metadata):
        """
        Args:
            name (str): predictor object name
            X (pandas.DataFrame): features in DataFrame format.
            metadata (dict): information about the data and code used to produce features
        """
        super().__init__(name, X, metadata)
        self.name = name
        self.X = X
        self.metadata = metadata

    @classmethod
    def validate_data(cls, processed_cycler_run, params_dict=None):
        """
        This function determines if the input data has the necessary attributes for
        creation of this feature class. It should test for all of the possible reasons
        that feature generation would fail for this particular input data.

        Args:
            processed_cycler_run (beep.structure.ProcessedCyclerRun): data from cycler run
            params_dict (dict): dictionary of parameters governing how the ProcessedCyclerRun object
                gets featurized. These could be filters for column or row operations

        Returns:
            bool: True/False indication of ability to proceed with feature generation
        """
        if params_dict is None:
            params_dict = FEATURE_HYPERPARAMS[cls.class_feature_name]
        conditions = []
        if not hasattr(processed_cycler_run, "diagnostic_summary") & hasattr(
            processed_cycler_run, "diagnostic_data"
        ):
            return False
        if processed_cycler_run.diagnostic_summary is None:
            return False
        elif processed_cycler_run.diagnostic_summary.empty:
            return False
        else:
            df = processed_cycler_run.diagnostic_summary
            df = df[df.cycle_type == params_dict["diagnostic_cycle_type"]]
            conditions.append(
                df.cycle_index.nunique() >= max(params_dict["diag_pos_list"]) + 1
            )

        return all(conditions)

    @classmethod
    def get_summary_diff(cls, processed_cycler_run,
                         pos=None,
                         cycle_types=None,
                         metrics=None):
        """
        Helper function to calculate difference between summary values in the diagnostic cycles

                Args:
                    processed_cycler_run (beep.structure.ProcessedCyclerRun)
                    pos (list): position of the diagnostics to use in the calculation
                    cycle_types (list): calculate difference for these diagnostic types
                    metrics (str): Calculate difference for these metrics

                Returns:
                    values (list): List of difference values to insert into the dataframe
                    names (list): List of column headers to use in the creation of the dataframe
                """
        if pos is None:
            pos = [0, 1]
        if cycle_types is None:
            cycle_types = ["rpt_0.2C", "rpt_1C", "rpt_2C"]
        if metrics is None:
            metrics = ["discharge_capacity", "discharge_energy", "charge_capacity", "charge_energy"]

        values = []
        names = []
        for cycle_type in cycle_types:
            diag_type_summary = processed_cycler_run.diagnostic_summary[
                processed_cycler_run.diagnostic_summary.cycle_type == cycle_type]
            for metric in metrics:
                diff = (diag_type_summary.iloc[pos[1]][metric] - diag_type_summary.iloc[pos[0]][metric]) \
                       / diag_type_summary.iloc[pos[0]][metric]
                values.append(diff)
                names.append("diag_sum_diff_" + str(pos[0]) + "_" + str(pos[1]) + "_" + cycle_type + metric)
        return values, names

    @classmethod
    def features_from_processed_cycler_run(cls, processed_cycler_run, params_dict=None,
                                           parameters_path="data-share/raw/parameters"):
        """
        Generate features listed in early prediction manuscript using both diagnostic and regular cycles

        Args:
            processed_cycler_run (beep.structure.ProcessedCyclerRun)
            params_dict (dict): dictionary of parameters governing how the ProcessedCyclerRun object
                gets featurized. These could be filters for column or row operations
            parameters_path (str): Root directory storing project parameter files.

        Returns:
            X (pd.DataFrame): Dataframe containing the feature
        """
        if params_dict is None:
            params_dict = FEATURE_HYPERPARAMS[cls.class_feature_name]

        # Filter out "final" diagnostic cycles that have been appended to the end of the file with the wrong
        # cycle number(test time is monotonic)
        processed_cycler_run.diagnostic_data = processed_cycler_run.diagnostic_data[
            ~((processed_cycler_run.diagnostic_data.test_time > params_dict['test_time_filter_sec']) &
              (processed_cycler_run.diagnostic_data.cycle_index < params_dict['cycle_index_filter']))
        ]
        processed_cycler_run.diagnostic_data = processed_cycler_run.diagnostic_data.groupby(
            ["cycle_index", "step_index", "step_index_counter"]
        ).filter(lambda x: ~x["test_time"].isnull().all())

        diag_intrp = processed_cycler_run.diagnostic_data

        X = pd.DataFrame(np.zeros((1, 54)))

        # Calculate the cycles and the steps for the selected diagnostics
        cycles = diag_intrp.cycle_index[diag_intrp.cycle_type ==
                                        params_dict["diagnostic_cycle_type"]].unique()
        step_dict_0 = featurizer_helpers.get_step_index(processed_cycler_run,
                                                        cycle_type=params_dict["diagnostic_cycle_type"],
                                                        diag_pos=params_dict["diag_pos_list"][0])
        step_dict_1 = featurizer_helpers.get_step_index(processed_cycler_run,
                                                        cycle_type=params_dict["diagnostic_cycle_type"],
                                                        diag_pos=params_dict["diag_pos_list"][1])

        # Create masks for each position in the data
        mask_pos_0_charge = ((diag_intrp.cycle_index == cycles[params_dict["diag_pos_list"][0]]) &
                             (diag_intrp.step_index == step_dict_0[params_dict["diagnostic_cycle_type"] + '_charge']))
        mask_pos_1_charge = ((diag_intrp.cycle_index == cycles[params_dict["diag_pos_list"][1]]) &
                             (diag_intrp.step_index == step_dict_1[params_dict["diagnostic_cycle_type"] + '_charge']))
        mask_pos_0_discharge = ((diag_intrp.cycle_index == cycles[params_dict["diag_pos_list"][0]]) &
                                (diag_intrp.step_index ==
                                 step_dict_0[params_dict["diagnostic_cycle_type"] + '_discharge']))
        mask_pos_1_discharge = ((diag_intrp.cycle_index == cycles[params_dict["diag_pos_list"][1]]) &
                                (diag_intrp.step_index ==
                                 step_dict_1[params_dict["diagnostic_cycle_type"] + '_discharge']))

        # Charging Capacity features
        Qc_1 = diag_intrp.charge_capacity[mask_pos_1_charge]
        Qc_0 = diag_intrp.charge_capacity[mask_pos_0_charge]
        QcDiff = Qc_1.values - Qc_0.values
        QcDiff = QcDiff[~np.isnan(QcDiff)]

        X.loc[0, 0:6] = cls.get_summary_statistics(QcDiff)

        # Discharging Capacity features
        Qd_1 = diag_intrp.discharge_capacity[mask_pos_1_discharge]
        Qd_0 = diag_intrp.discharge_capacity[mask_pos_0_discharge]
        QdDiff = Qd_1.values - Qd_0.values
        QdDiff = QdDiff[~np.isnan(QdDiff)]

        X.loc[0, 7:13] = cls.get_summary_statistics(QdDiff)

        # Charging Energy features
        Ec_1 = diag_intrp.charge_energy[mask_pos_1_charge]
        Ec_0 = diag_intrp.charge_energy[mask_pos_0_charge]
        EcDiff = Ec_1.values - Ec_0.values
        EcDiff = EcDiff[~np.isnan(EcDiff)]

        X.loc[0, 14:20] = cls.get_summary_statistics(EcDiff)

        # Discharging Energy features
        Ed_1 = diag_intrp.discharge_energy[mask_pos_1_discharge]
        Ed_0 = diag_intrp.discharge_energy[mask_pos_0_discharge]
        EdDiff = Ed_1.values - Ed_0.values
        EdDiff = EdDiff[~np.isnan(EdDiff)]

        X.loc[0, 21:27] = cls.get_summary_statistics(EdDiff)

        # Charging dQdV features
        dQdVc_1 = diag_intrp.charge_dQdV[mask_pos_1_charge]
        dQdVc_0 = diag_intrp.charge_dQdV[mask_pos_0_charge]
        dQdVcDiff = dQdVc_1.values - dQdVc_0.values
        dQdVcDiff = dQdVcDiff[~np.isnan(dQdVcDiff)]

        X.loc[0, 28:34] = cls.get_summary_statistics(dQdVcDiff)

        # Discharging Capacity features
        dQdVd_1 = diag_intrp.discharge_dQdV[mask_pos_1_discharge]
        dQdVd_0 = diag_intrp.discharge_dQdV[mask_pos_0_discharge]
        dQdVdDiff = dQdVd_1.values - dQdVd_0.values
        dQdVdDiff = dQdVdDiff[~np.isnan(dQdVdDiff)]

        X.loc[0, 35:41] = cls.get_summary_statistics(dQdVdDiff)

        X.loc[0, 42:53], names = cls.get_summary_diff(processed_cycler_run, params_dict["diag_pos_list"])

        operations = ["var", "min", "mean", "skew", "kurtosis", "abs", "square"]
        quantities = [
            "charging_capacity",
            "discharging_capacity",
            "charging_energy",
            "discharging_energy",
            "charging_dQdV",
            "discharging_dQdV",
        ]

        X.columns = [y + "_" + x for x in quantities for y in operations] + names
        return X


class DeltaQFastCharge(BeepFeatures):
    """
    Object corresponding to feature object. Includes constructors
    to create the features, object names and metadata attributes in the
    object
        name (str): predictor object name.
        X (pandas.DataFrame): features in DataFrame format.
        metadata (dict): information about the conditions, data
            and code used to produce features
    """

    # Class name for the feature object
    class_feature_name = "DeltaQFastCharge"

    def __init__(self, name, X, metadata):
        """
        Args:
            name (str): predictor object name
            X (pandas.DataFrame): features in DataFrame format.
            metadata (dict): information about the data and code used to produce features
        """
        super().__init__(name, X, metadata)
        self.name = name
        self.X = X
        self.metadata = metadata

    @classmethod
    def validate_data(cls, processed_cycler_run, params_dict=None):
        """
        This function determines if the input data has the necessary attributes for
        creation of this feature class. It should test for all of the possible reasons
        that feature generation would fail for this particular input data.

        Args:
            processed_cycler_run (beep.structure.ProcessedCyclerRun): data from cycler run
            params_dict (dict): dictionary of parameters governing how the ProcessedCyclerRun object
            gets featurized. These could be filters for column or row operations
        Returns:
            bool: True/False indication of ability to proceed with feature generation
        """

        if params_dict is None:
            params_dict = FEATURE_HYPERPARAMS[cls.class_feature_name]

        conditions = list()

        conditions.append(
            processed_cycler_run.structured_summary.index.max()
            > params_dict["final_pred_cycle"]
        )
        conditions.append(
            processed_cycler_run.structured_summary.index.min()
            <= params_dict["init_pred_cycle"]
        )
        conditions.append("cycle_index" in processed_cycler_run.structured_summary.columns)
        conditions.append("cycle_index" in processed_cycler_run.structured_data.columns)

        return all(conditions)

    @classmethod
    def features_from_processed_cycler_run(cls, processed_cycler_run, params_dict=None,
                                           parameters_path="data-share/raw/parameters"):
        """
        Generate features listed in early prediction manuscript, primarily related to the
        so called delta Q feature
        Args:
            processed_cycler_run (beep.structure.ProcessedCyclerRun): data from cycler run
            params_dict (dict): dictionary of parameters governing how the ProcessedCyclerRun object
                gets featurized. These could be filters for column or row operations
            parameters_path (str): Root directory storing project parameter files.

        Returns:
            pd.DataFrame: features indicative of degradation, derived from the input data
        """

        if params_dict is None:
            params_dict = FEATURE_HYPERPARAMS[cls.class_feature_name]

        assert params_dict["mid_pred_cycle"] > 10  # Sufficient cycles for analysis
        assert (
            params_dict["final_pred_cycle"] > params_dict["mid_pred_cycle"]
        )  # Must have final_pred_cycle > mid_pred_cycle

        i_final = params_dict["final_pred_cycle"] - 1  # python indexing
        i_mid = params_dict["mid_pred_cycle"] - 1

        summary = processed_cycler_run.structured_summary
        params_dict[
            "n_nominal_cycles"
        ] = 40  # For nominal capacity, use median discharge capacity of first n cycles

        if "step_type" in processed_cycler_run.structured_data.columns:
            interpolated_df = processed_cycler_run.structured_data[
                processed_cycler_run.structured_data.step_type == "discharge"
            ]
        else:
            interpolated_df = processed_cycler_run.structured_data
        X = pd.DataFrame(np.zeros((1, 20)))
        labels = []
        # Discharge capacity, cycle 2 = Q(n=2)
        X[0] = summary.discharge_capacity.iloc[1]
        labels.append("discharge_capacity_cycle_2")

        # Max discharge capacity - discharge capacity, cycle 2 = max_n(Q(n)) - Q(n=2)
        X[1] = max(
            summary.discharge_capacity.iloc[np.arange(i_final + 1)]
            - summary.discharge_capacity.iloc[1]
        )
        labels.append("max_discharge_capacity_difference")

        # Discharge capacity, cycle 100 = Q(n=100)
        X[2] = summary.discharge_capacity.iloc[i_final]
        labels.append("discharge_capacity_cycle_100")

        # Feature representing time-temperature integral over cycles 2 to 100
        X[3] = np.nansum(summary.time_temperature_integrated.iloc[np.arange(i_final + 1)])
        labels.append("integrated_time_temperature_cycles_1:100")

        # Mean of charge times of first 5 cycles
        X[4] = np.nanmean(summary.charge_duration.iloc[1:6])
        labels.append("charge_time_cycles_1:5")

        # Descriptors based on capacity loss between cycles 10 and 100.
        Qd_final = interpolated_df.discharge_capacity[
            interpolated_df.cycle_index == i_final
        ]
        Qd_10 = interpolated_df.discharge_capacity[interpolated_df.cycle_index == 9]

        Qd_diff = Qd_final.values - Qd_10.values

        # If DeltaQ(V) is not an empty array, compute summary stats, else initialize with np.nan
        # Cells discharged rapidly over a narrow voltage window run into have no interpolated discharge steps
        if len(Qd_diff):
            X[5] = np.log10(np.abs(np.nanmin(Qd_diff)))  # Minimum
            X[6] = np.log10(np.abs(np.nanmean(Qd_diff)))  # Mean
            X[7] = np.log10(np.abs(np.nanvar(Qd_diff)))  # Variance
            X[8] = np.log10(np.abs(skew(Qd_diff)))  # Skewness
            X[9] = np.log10(np.abs(kurtosis(Qd_diff)))  # Kurtosis
            X[10] = np.log10(np.abs(Qd_diff[0]))  # First difference
        else:
            X[5:11] = np.nan

        labels.append("abs_min_discharge_capacity_difference_cycles_2:100")
        labels.append("abs_mean_discharge_capacity_difference_cycles_2:100")
        labels.append("abs_variance_discharge_capacity_difference_cycles_2:100")
        labels.append("abs_skew_discharge_capacity_difference_cycles_2:100")
        labels.append("abs_kurtosis_discharge_capacity_difference_cycles_2:100")
        labels.append("abs_first_discharge_capacity_difference_cycles_2:100")

        X[11] = np.max(summary.temperature_maximum.iloc[list(range(1, i_final + 1))])  # Max T
        labels.append("max_temperature_cycles_1:100")

        X[12] = np.min(summary.temperature_minimum.iloc[list(range(1, i_final + 1))])  # Min T
        labels.append("min_temperature_cycles_1:100")

        # Slope and intercept of linear fit to discharge capacity as a fn of cycle #, cycles 2 to 100

        X[13], X[14] = np.polyfit(
            list(range(1, i_final + 1)),
            summary.discharge_capacity.iloc[list(range(1, i_final + 1))],
            1,
        )

        labels.append("slope_discharge_capacity_cycle_number_2:100")
        labels.append("intercept_discharge_capacity_cycle_number_2:100")

        # Slope and intercept of linear fit to discharge capacity as a fn of cycle #, cycles 91 to 100
        X[15], X[16] = np.polyfit(
            list(range(i_mid, i_final + 1)),
            summary.discharge_capacity.iloc[list(range(i_mid, i_final + 1))],
            1,
        )
        labels.append("slope_discharge_capacity_cycle_number_91:100")
        labels.append("intercept_discharge_capacity_cycle_number_91:100")

        IR_trend = summary.dc_internal_resistance.iloc[list(range(1, i_final + 1))]
        if any(v == 0 for v in IR_trend):
            IR_trend[IR_trend == 0] = np.nan

        # Internal resistance minimum
        X[17] = np.nanmin(IR_trend)
        labels.append("min_internal_resistance_cycles_2:100")

        # Internal resistance at cycle 2
        X[18] = summary.dc_internal_resistance.iloc[1]
        labels.append("internal_resistance_cycle_2")

        # Internal resistance at cycle 100 - cycle 2
        X[19] = (
            summary.dc_internal_resistance.iloc[i_final] - summary.dc_internal_resistance.iloc[1]
        )
        labels.append("internal_resistance_difference_cycles_2:100")

        # Nominal capacity
        X[20] = np.median(
            summary.discharge_capacity.iloc[0: params_dict["n_nominal_cycles"]]
        )
        labels.append("nominal_capacity_by_median")

        X.columns = labels
        return X


class TrajectoryFastCharge(DeltaQFastCharge):
    """
    Object corresponding to cycle numbers at which the capacity drops below
     specific percentages of the initial capacity. Computed on the discharge
     portion of the regular fast charge cycles.


    """

    # Class name for the feature object
    class_feature_name = "TrajectoryFastCharge"

    def __init__(self, name, X, metadata):
        """
        Invokes a TrajectoryFastCharge object

        Args:
            name (str): predictor object name.
            X (pandas.DataFrame): features in DataFrame format.
            metadata (dict): information about the conditions, data
                and code used to produce features

        """
        super().__init__(name, X, metadata)
        self.name = name
        self.X = X
        self.metadata = metadata

    @classmethod
    def validate_data(cls, processed_cycler_run, params_dict=None):
        """
        This function determines if the input data has the necessary attributes for
        creation of this feature class. It should test for all of the possible reasons
        that feature generation would fail for this particular input data.

        Args:
            processed_cycler_run (beep.structure.ProcessedCyclerRun): data from cycler run
            params_dict (dict): dictionary of parameters governing how the ProcessedCyclerRun object
            gets featurized. These could be filters for column or row operations
        Returns:
            bool: True/False indication of ability to proceed with feature generation
        """

        if params_dict is None:
            params_dict = FEATURE_HYPERPARAMS[cls.class_feature_name]

        conditions = []
        cap = processed_cycler_run.structured_summary.discharge_capacity
        conditions.append(cap.min() / cap.max() < params_dict["thresh_max_cap"])

        return all(conditions)

    @classmethod
    def features_from_processed_cycler_run(cls, processed_cycler_run, params_dict=None,
                                           parameters_path="data-share/raw/parameters"):
        """
        Calculate the outcomes from the input data. In particular, the number of cycles
        where we expect to reach certain thresholds of capacity loss
        Args:
            processed_cycler_run (beep.structure.ProcessedCyclerRun): data from cycler run
            params_dict (dict): dictionary of parameters governing how the ProcessedCyclerRun object
            gets featurized. These could be filters for column or row operations
            parameters_path (str): Root directory storing project parameter files.

        Returns:
            pd.DataFrame: cycles at which capacity/energy degradation exceeds thresholds
        """
        if params_dict is None:
            params_dict = FEATURE_HYPERPARAMS[cls.class_feature_name]
        y = processed_cycler_run.capacities_to_cycles(
            params_dict["thresh_max_cap"],
            params_dict["thresh_min_cap"],
            params_dict["interval_cap"],
        )
        return y


class DiagnosticProperties(BeepFeatures):
    """
    This class stores fractional levels of degradation in discharge capacity and discharge energy
    relative to the first cycle at each diagnostic cycle, grouped by diagnostic cycle type.

        name (str): predictor object name.
        X (pandas.DataFrame): features in DataFrame format.
        metadata (dict): information about the conditions, data
            and code used to produce features
    """

    # Class name for the feature object
    class_feature_name = "DiagnosticProperties"

    def __init__(self, name, X, metadata):
        super().__init__(name, X, metadata)
        self.name = name
        self.X = X
        self.metadata = metadata

    @classmethod
    def validate_data(cls, processed_cycler_run, params_dict=None):
        """
        This function determines if the input data has the necessary attributes for
        creation of this feature class. It should test for all of the possible reasons
        that feature generation would fail for this particular input data.

        Args:
            processed_cycler_run (beep.structure.ProcessedCyclerRun): data from cycler run
            params_dict (dict): dictionary of parameters governing how the ProcessedCyclerRun object
            gets featurized. These could be filters for column or row operations
        Returns:
            bool: True/False indication of ability to proceed with feature generation
        """
        if not hasattr(processed_cycler_run, "diagnostic_summary") & hasattr(
            processed_cycler_run, "diagnostic_data"
        ):
            return False
        if processed_cycler_run.diagnostic_summary is None:
            return False
        elif processed_cycler_run.diagnostic_summary.empty:
            return False
        else:
            return True

    @classmethod
    def features_from_processed_cycler_run(cls, processed_cycler_run, params_dict=None,
                                           parameters_path="data-share/raw/parameters"):
        """
        Generates diagnostic-property features from processed cycler run, including values for n*x method
        Args:
            processed_cycler_run (beep.structure.ProcessedCyclerRun): data from cycler run
            params_dict (dict): dictionary of parameters governing how the ProcessedCyclerRun object
            gets featurized. These could be filters for column or row operations
            parameters_path (str): Root directory storing project parameter files.

        Returns:
            pd.DataFrame: with "cycle_index", "fractional_metric", "x", "n", "cycle_type" and "metric" columns, rows
            for each diagnostic cycle of the cell
        """
        if params_dict is None:
            params_dict = FEATURE_HYPERPARAMS[cls.class_feature_name]

        cycle_types = processed_cycler_run.diagnostic_summary.cycle_type.unique()
        X = pd.DataFrame()
        for quantity in params_dict["quantities"]:
            for cycle_type in cycle_types:
                summary_diag_cycle_type = featurizer_helpers.get_fractional_quantity_remaining_nx(
                    processed_cycler_run, quantity, cycle_type, parameters_path=parameters_path
                )

                summary_diag_cycle_type.loc[:, "cycle_type"] = cycle_type
                summary_diag_cycle_type.loc[:, "metric"] = quantity
                X = X.append(summary_diag_cycle_type)

        return X


class DegradationPredictor(MSONable):
    """
    Object corresponding to feature matrix. Includes constructors
    to initialize the feature vectors.
    Attributes:
        name (str): predictor object name.
        X (pandas.DataFrame): data as records x features.
        y (pandas.DataFrame): targets.
        feature_labels (list): feature labels.
        predict_only (bool): True/False to specify predict/train mode.
        prediction_type (str): Type of regression - 'single' vs 'multi'.
        predicted_quantity (str): 'cycle' or 'capacity'.
        nominal_capacity (float):
    """

    def __init__(
        self,
        name,
        X,
        feature_labels=None,
        y=None,
        nominal_capacity=1.1,
        predict_only=False,
        predicted_quantity="cycle",
        prediction_type="multi",
    ):
        """
        Args:
            name (str): predictor object name
            X (pandas.DataFrame): features in DataFrame format.
            name (str): name of method for featurization.
            y (pandas.Dataframe or float): one or more outcomes.
            predict_only (bool): True/False to specify predict/train mode.
            predicted_quantity (str): 'cycle' or 'capacity'.
            prediction_type (str): Type of regression - 'single' vs 'multi'.
        """
        self.name = name
        self.X = X
        self.feature_labels = feature_labels
        self.predict_only = predict_only
        self.prediction_type = prediction_type
        self.predicted_quantity = predicted_quantity
        self.y = y
        self.nominal_capacity = nominal_capacity

    @classmethod
    def from_processed_cycler_run_file(
        cls,
        path,
        features_label="full_model",
        predict_only=False,
        predicted_quantity="cycle",
        prediction_type="multi",
        diagnostic_features=False,
    ):
        """
        Args:
            path (str): string corresponding to file path with ProcessedCyclerRun object.
            features_label (str): name of method for featurization.
            predict_only (bool): True/False to specify predict/train mode.
            predicted_quantity (str): 'cycle' or 'capacity'.
            prediction_type (str): Type of regression - 'single' vs 'multi'.
            diagnostic_features (bool): whether to compute diagnostic features.
        """
        processed_cycler_run = auto_load_processed(path)

        if features_label == "full_model":
            return cls.init_full_model(
                processed_cycler_run,
                predict_only=predict_only,
                predicted_quantity=predicted_quantity,
                diagnostic_features=diagnostic_features,
                prediction_type=prediction_type,
            )
        else:
            raise NotImplementedError

    @classmethod
    def init_full_model(
        cls,
        processed_cycler_run,
        init_pred_cycle=10,
        mid_pred_cycle=91,
        final_pred_cycle=100,
        predict_only=False,
        prediction_type="multi",
        predicted_quantity="cycle",
        diagnostic_features=False,
    ):
        """
        Generate features listed in early prediction manuscript
        Args:
            processed_cycler_run (beep.structure.ProcessedCyclerRun): information about cycler run
            init_pred_cycle (int): index of initial cycle index used for predictions
            mid_pred_cycle (int): index of intermediate cycle index used for predictions
            final_pred_cycle (int): index of highest cycle index used for predictions
            predict_only (bool): whether or not to include cycler life in the object
            prediction_type (str): 'single': cycle life to reach 80% capacity.
                                   'multi': remaining capacity at fixed cycles
            predicted_quantity (str): quantity being predicted - cycles/capacity
            diagnostic_features (bool): whether or not to compute diagnostic features
        Returns:
            beep.featurize.DegradationPredictor: DegradationPredictor corresponding to the ProcessedCyclerRun file.
        """
        assert mid_pred_cycle > 10, "Insufficient cycles for analysis"
        assert (
            final_pred_cycle > mid_pred_cycle
        ), "Must have final_pred_cycle > mid_pred_cycle"
        i_final = final_pred_cycle - 1  # python indexing
        i_mid = mid_pred_cycle - 1
        summary = processed_cycler_run.structured_summary
        assert (
            len(processed_cycler_run.structured_summary) > final_pred_cycle
        ), "cycle count must exceed final_pred_cycle"
        cycles_to_average_over = (
            40  # For nominal capacity, use median discharge capacity of first n cycles
        )

        # Features in "nature energy" set only use discharge portion of the cycle
        if "step_type" in processed_cycler_run.structured_data.columns:
            interpolated_df = processed_cycler_run.structured_data[
                processed_cycler_run.structured_data.step_type == "discharge"
            ]
        else:
            interpolated_df = processed_cycler_run.structured_data

        X = pd.DataFrame(np.zeros((1, 20)))
        labels = []
        # Discharge capacity, cycle 2 = Q(n=2)
        X[0] = summary.discharge_capacity[1]
        labels.append("discharge_capacity_cycle_2")

        # Max discharge capacity - discharge capacity, cycle 2 = max_n(Q(n)) - Q(n=2)
        X[1] = max(
            summary.discharge_capacity[np.arange(final_pred_cycle)]
            - summary.discharge_capacity[1]
        )
        labels.append("max_discharge_capacity_difference")

        # Discharge capacity, cycle 100 = Q(n=100)
        X[2] = summary.discharge_capacity[i_final]
        labels.append("discharge_capacity_cycle_100")

        # Feature representing time-temperature integral over cycles 2 to 100
        X[3] = np.nansum(
            summary.time_temperature_integrated[np.arange(final_pred_cycle)]
        )
        labels.append("integrated_time_temperature_cycles_1:100")

        # Mean of charge times of first 5 cycles
        X[4] = np.nanmean(summary.charge_duration[1:6])
        labels.append("charge_time_cycles_1:5")

        # Descriptors based on capacity loss between cycles 10 and 100.
        Qd_final = interpolated_df.discharge_capacity[
            interpolated_df.cycle_index == i_final
        ]
        Qd_10 = interpolated_df.discharge_capacity[interpolated_df.cycle_index == 9]

        Qd_diff = Qd_final.values - Qd_10.values

        X[5] = np.log10(np.abs(np.min(Qd_diff)))  # Minimum
        labels.append("abs_min_discharge_capacity_difference_cycles_2:100")

        X[6] = np.log10(np.abs(np.mean(Qd_diff)))  # Mean
        labels.append("abs_mean_discharge_capacity_difference_cycles_2:100")

        X[7] = np.log10(np.abs(np.var(Qd_diff)))  # Variance
        labels.append("abs_variance_discharge_capacity_difference_cycles_2:100")

        X[8] = np.log10(np.abs(skew(Qd_diff)))  # Skewness
        labels.append("abs_skew_discharge_capacity_difference_cycles_2:100")

        X[9] = np.log10(np.abs(kurtosis(Qd_diff)))  # Kurtosis
        labels.append("abs_kurtosis_discharge_capacity_difference_cycles_2:100")

        X[10] = np.log10(np.abs(Qd_diff[0]))  # First difference
        labels.append("abs_first_discharge_capacity_difference_cycles_2:100")

        X[11] = max(
            summary.temperature_maximum[list(range(1, final_pred_cycle))]
        )  # Max T
        labels.append("max_temperature_cycles_1:100")

        X[12] = min(
            summary.temperature_minimum[list(range(1, final_pred_cycle))]
        )  # Min T
        labels.append("min_temperature_cycles_1:100")

        # Slope and intercept of linear fit to discharge capacity as a fn of cycle #, cycles 2 to 100

        X[13], X[14] = np.polyfit(
            list(range(1, final_pred_cycle)),
            summary.discharge_capacity[list(range(1, final_pred_cycle))],
            1,
        )

        labels.append("slope_discharge_capacity_cycle_number_2:100")
        labels.append("intercept_discharge_capacity_cycle_number_2:100")

        # Slope and intercept of linear fit to discharge capacity as a fn of cycle #, cycles 91 to 100
        X[15], X[16] = np.polyfit(
            list(range(i_mid, final_pred_cycle)),
            summary.discharge_capacity[list(range(i_mid, final_pred_cycle))],
            1,
        )
        labels.append("slope_discharge_capacity_cycle_number_91:100")
        labels.append("intercept_discharge_capacity_cycle_number_91:100")

        IR_trend = summary.dc_internal_resistance[list(range(1, final_pred_cycle))]
        if any(v == 0 for v in IR_trend):
            IR_trend[IR_trend == 0] = np.nan

        # Internal resistance minimum
        X[17] = np.nanmin(IR_trend)
        labels.append("min_internal_resistance_cycles_2:100")

        # Internal resistance at cycle 2
        X[18] = summary.dc_internal_resistance[1]
        labels.append("internal_resistance_cycle_2")

        # Internal resistance at cycle 100 - cycle 2
        X[19] = (
            summary.dc_internal_resistance[i_final] - summary.dc_internal_resistance[1]
        )
        labels.append("internal_resistance_difference_cycles_2:100")

        X.columns = labels
        if predict_only:
            y = None
        else:
            if prediction_type == "single":
                y = processed_cycler_run.get_cycle_life()
            elif prediction_type == "multi":
                if predicted_quantity == "cycle":
                    y = processed_cycler_run.capacities_to_cycles(
                        thresh_max_cap=0.98, thresh_min_cap=0.78, interval_cap=0.03
                    )
                elif predicted_quantity == "capacity":
                    y = processed_cycler_run.cycles_to_capacities()
                else:
                    raise NotImplementedError(
                        "{} predicted_quantity type not implemented".format(
                            predicted_quantity
                        )
                    )
        nominal_capacity = np.median(
            summary.discharge_capacity.iloc[0:cycles_to_average_over]
        )

        return cls(
            "full_model",
            X,
            feature_labels=labels,
            y=y,
            nominal_capacity=nominal_capacity,
            predict_only=predict_only,
            prediction_type=prediction_type,
            predicted_quantity=predicted_quantity,
        )

    def as_dict(self):
        """
        Method for dictionary serialization
        Returns:
            dict: corresponding to dictionary for serialization
        """
        obj = {
            "@module": self.__class__.__module__,
            "@class": self.__class__.__name__,
            "name": self.name,
            "X": self.X.to_dict("list"),
            "feature_labels": self.feature_labels,
            "predict_only": self.predict_only,
            "prediction_type": self.prediction_type,
            "nominal_capacity": self.nominal_capacity,
        }
        if isinstance(self.y, pd.DataFrame):
            obj["y"] = self.y.to_dict("list")
        else:
            obj["y"] = self.y
        return obj

    @classmethod
    def from_dict(cls, d):
        """MSONable deserialization method"""
        d["X"] = pd.DataFrame(d["X"])
        return cls(**d)


def add_file_prefix_to_path(path, prefix):
    """
    Helper function to add file prefix to path.

    Args:
        path (str): full path to file.
        prefix (str): prefix for file.

    Returns:
        str: path with prefix appended to filename.

    """
    split_path = list(os.path.split(path))
    split_path[-1] = prefix + split_path[-1]
    return os.path.join(*split_path)


def process_file_list_from_json(file_list_json, processed_dir="data-share/features/"):
    """
    Function to take a json file containing processed cycler run file locations,
    extract features, dump the processed file into a predetermined directory,
    and return a jsonable dict of feature file locations.

    Args:
        file_list_json (str): json string or json filename corresponding
            to a dictionary with a file_list attribute,
            if this string ends with ".json", a json file is assumed
            and loaded, otherwise interpreted as a json string.
        processed_dir (str): location for processed cycler run output files
            to be placed.

    Returns:
        str: json string of feature files (with key "file_list").

    """
    # Get file list and validity from json, if ends with .json,
    # assume it's a file, if not assume it's a json string
    if file_list_json.endswith(".json"):
        file_list_data = loadfn(file_list_json)
    else:
        file_list_data = json.loads(file_list_json)

    # Setup workflow
    outputs = WorkflowOutputs()

    # Add root path to processed_dir
    processed_dir = os.path.join(
        os.environ.get("BEEP_PROCESSING_DIR", "/"), processed_dir
    )
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    file_list = file_list_data["file_list"]
    run_ids = file_list_data["run_list"]
    processed_run_list = []
    processed_result_list = []
    processed_message_list = []
    processed_paths_list = []

    for path, run_id in zip(file_list, run_ids):
        logger.info("run_id=%s featurizing=%s", str(run_id), path, extra=s)
        processed_cycler_run = auto_load_processed(path)

        featurizer_classes = [
            HPPCResistanceVoltageFeatures,
            DiagnosticSummaryStats,
            DeltaQFastCharge,
            TrajectoryFastCharge,
            DiagnosticProperties,
            intracell_losses.IntracellCycles,
            intracell_losses.IntracellFeatures,
        ]

        for featurizer_class in featurizer_classes:
            if featurizer_class.class_feature_name in FEATURE_HYPERPARAMS.keys():
                params_dict = FEATURE_HYPERPARAMS[featurizer_class.class_feature_name]
            else:
                params_dict = None
            featurizer = featurizer_class.from_run(
                path, processed_dir, processed_cycler_run, params_dict
            )
            if featurizer:
                dumpfn(featurizer, featurizer.name)
                processed_paths_list.append(featurizer.name)
                processed_run_list.append(run_id)
                processed_result_list.append("success")
                processed_message_list.append({"comment": "", "error": ""})
                logger.info("Successfully generated %s", featurizer.name, extra=s)
            else:
                processed_paths_list.append(path)
                processed_run_list.append(run_id)
                processed_result_list.append("incomplete")
                processed_message_list.append(
                    {
                        "comment": "Insufficient or incorrect data for featurization",
                        "error": "",
                    }
                )
                logger.info("Unable to featurize %s", path, extra=s)

    output_data = {
        "file_list": processed_paths_list,
        "run_list": processed_run_list,
        "result_list": processed_result_list,
        "message_list": processed_message_list,
    }

    # Workflow outputs
    outputs.put_workflow_outputs_list(output_data, "featurizing")

    # Return jsonable file list
    return json.dumps(output_data)


def main():
    """
    Main function of this module, takes in arguments of an input
    and output filename corresponding to structured cycler run data
    and creates a predictor object output for analysis/ML processing

    Returns:
        None

    """
    # Parse args and construct initial cycler run
    logger.info("starting", extra=s)
    logger.info("Running version=%s", __version__, extra=s)
    try:
        args = docopt(__doc__)
        input_json = args["INPUT_JSON"]
        print(process_file_list_from_json(input_json), end="")
    except Exception as e:
        logger.error(str(e), extra=s)
        raise e
    logger.info("finish", extra=s)

    return None


if __name__ == "__main__":
    main()
