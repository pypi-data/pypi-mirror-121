import pandas as pd
from typing import List


def merge_two_df(
        df1: pd.DataFrame,
        df2: pd.DataFrame,
        on: str
) -> pd.DataFrame:
    return df1.merge(df2, on=on)


def remove_features(df: pd.DataFrame, features: List[str]) -> pd.DataFrame:
    return df.drop(columns=features, axis=1)


def cast_series_to_datetime(
        df: pd.DataFrame,
        column_name: str,
        date_format: str = "%Y-%m-%d"
) -> pd.DataFrame:
    df[column_name] = pd.to_datetime(df[column_name], format=date_format)
    return df


def create_year_and_week_column(
        df: pd.DataFrame,
        column_name: str
) -> pd.DataFrame:
    df["year"] = df[column_name].dt.year
    df["week_number"] = df[column_name].dt.week
    return df


def sum_turnover_by_week_bu_dpt(
        df: pd.DataFrame,
        features: List[str] =
        ["but_num_business_unit", "dpt_num_department", "year", "week_number"],
        column_to_sum: str = "turnover"
) -> pd.DataFrame:
    return (
        df
        .groupby(features, as_index=False)
        .agg({column_to_sum: "sum"})
    )


def create_id_bu_dpt(df: pd.DataFrame) -> pd.DataFrame:
    df["but_bu_dpt_id"] = (
            df["but_num_business_unit"].astype(str)
            + "-"
            + df["dpt_num_department"].astype(str)
    )
    return df


def create_id_year_week_number(df: pd.DataFrame) -> pd.DataFrame:
    df["ds"] = (
            df["year"].astype(str)
            + "-"
            + df["week_number"].astype(str)
    )
    return df


def create_date_from_year_and_week_number(df: pd.DataFrame) -> pd.DataFrame:
    df["ds"] = (
        pd.to_datetime(
            df["ds"] + "-1",
            format="%Y-%W-%w"
        )
    )
    return df


def rename_taget_column(
        df: pd.DataFrame,
        target_col_to_rename: str
) -> pd.DataFrame:
    return df.rename(columns={target_col_to_rename: "y"})


def create_store_dpt_df(df: pd.DataFrame) -> List[pd.DataFrame]:
    return [df[df["but_bu_dpt_id"] == i] for i in df["but_bu_dpt_id"].unique()]


def select_columns_to_fit(
        dfs: List[pd.DataFrame],
        columns_to_fit: List[str] =
        ["ds", "y", "but_bu_dpt_id"]
) -> List[pd.DataFrame]:
    return [df[columns_to_fit] for df in dfs]


def remove_n_last_values(
        dfs: List[pd.DataFrame],
        n_value_to_remove: int = 8
) -> List[pd.DataFrame]:
    return [df.drop(df.tail(n_value_to_remove).index) for df in dfs]


def create_df_for_modeling(df: pd.DataFrame) -> List[pd.DataFrame]:
    df = sum_turnover_by_week_bu_dpt(df)
    df = create_id_bu_dpt(df)
    df = create_id_year_week_number(df)
    df = create_date_from_year_and_week_number(df)
    df = rename_taget_column(df, target_col_to_rename="turnover")

    df_list = create_store_dpt_df(df)
    df_list = remove_n_last_values(df_list)
    df_list = select_columns_to_fit(df_list)

    return df_list
