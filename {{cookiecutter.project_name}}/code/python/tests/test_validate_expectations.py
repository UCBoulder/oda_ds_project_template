import sys
from pathlib import Path

import pandas as pd
import pytest
from pandas.util.testing import makeMixedDataFrame
from pandas.testing import assert_frame_equal
from great_expectations.exceptions import GreatExpectationsError


# Ensures that the code in src can be run and accessed from the console:
# see importing sibling packages in Python
sys.path.append(str(Path(__file__).parents[1].resolve()))

from utils import validate_expectations

# TODO: Use df as a fixture
def test_validate_expectations_non_df():
    with pytest.raises(ValueError, match="must return a Pandas DataFrame$"):

        @validate_expectations(suite_name="person_status.json")
        def non_df():
            return makeMixedDataFrame().to_numpy()

        non_df()


def test_validate_expectations_suite_name_is_not_valid():
    with pytest.raises(ValueError, match="valid json expectation suite$"):

        @validate_expectations(suite_name="")
        def df():
            return makeMixedDataFrame()

        df()


def test_validate_expectations_suite_name_is_none():
    with pytest.raises(ValueError, match="A suite name is required"):

        @validate_expectations(suite_name=None)
        def df():
            return makeMixedDataFrame()

        df()


def test_validate_expectations_suite_name_not_found():
    with pytest.raises(FileNotFoundError, match="The suite could not be found"):

        @validate_expectations(suite_name="mytestsuite.json")
        def df():
            return makeMixedDataFrame()

        df()


def test_validate_expectations_df_does_not_meet_expectations():
    with pytest.raises(
        GreatExpectationsError, match="The dataframe did not meet expectations"
    ):

        @validate_expectations(suite_name="person_status.json")
        def df():
            return makeMixedDataFrame()

        df()


def test_validate_expectations_df_does_not_get_modified():
    df = pd.DataFrame(
        columns=[
            "person_id",
            "person_name",
            "person_created",
            "person_status",
            "status_timestamp",
        ]
    )

    @validate_expectations(suite_name="person_status.json")
    def result():
        return df

    expected = df

    assert_frame_equal(result(), expected)
