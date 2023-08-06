from forecasting_mle_decathlon.processing.processing import (
    merge_two_df,
    remove_features,
    cast_series_to_datetime,
    create_year_and_week_column
)
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest


@pytest.fixture
def df():
    return pd.DataFrame(
        [[1, "2021-09-10", 10], [2, "2021-10-10", 20]],
        columns=["id", "date", "value"]
    )


@pytest.fixture
def df_date(df):
    df["date"] = pd.to_datetime(df["date"])
    return df


def test_merge_two_df():
    # GIVEN
    df1 = pd.DataFrame(
        [[1, 1], [2, 1]],
        columns=["id", "value_df1"]
    )
    df2 = pd.DataFrame(
        [[1, 1], [2, 1]],
        columns=["id", "value_df2"]
    )
    expected = pd.DataFrame(
        [[1, 1, 1], [2, 1, 1]],
        columns=["id", "value_df1", "value_df2"]
    )
    merge_on = "id"

    # WHEN
    merge_result = merge_two_df(df1, df2, on=merge_on)

    # THEN
    assert_frame_equal(merge_result, expected)


def test_remove_features(df):
    # GIVEN
    feature_to_remove = ["date"]
    expected_columns = ["id", "value"]

    # WHEN
    result_df = remove_features(df, feature_to_remove)

    # THEN
    assert result_df.columns.values.tolist() == expected_columns


def test_cast_series_to_datetime(df):
    # GIVEN
    column_to_cast = "date"
    date_format = "%Y-%m-%d"
    expected_date_series = pd.Series(
        ["2021-09-10", "2021-10-10"]
    )
    expected_date_series = pd.to_datetime(expected_date_series)

    # WHEN
    result_series = cast_series_to_datetime(
        df,
        column_to_cast,
        date_format
    )[column_to_cast]

    # THEN
    assert (result_series.values.tolist() ==
            expected_date_series.values.tolist())


def test_create_year_and_week_column(df_date):
    # GIVEN
    column_name = "date"
    expected_df = pd.DataFrame(
        [[2021, 36], [2021, 40]],
        columns=["year", "week_number"]
    )
    # WHEN
    result_df = create_year_and_week_column(
        df_date,
        column_name
    )[["year", "week_number"]]

    # THEN
    assert_frame_equal(result_df, expected_df)

    pass
