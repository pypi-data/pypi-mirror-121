import pandas as pd
from typing import List, Tuple
from forecasting.processing.data_transformer import (
    DataframeFunctionTransformer
)
from forecasting.processing.processing import (
    merge_two_df,
    remove_features,
    cast_series_to_datetime,
    create_year_and_week_column,
    create_df_for_modeling
)


def create_processing_pipeline(
        bu_df: pd.DataFrame
) -> List[Tuple[str, DataframeFunctionTransformer]]:

    return [
        (
            'create_df',
            DataframeFunctionTransformer(
                merge_two_df,
                df2=bu_df,
                on="but_num_business_unit"
            )
        ),
        ('remove_correlated_features', DataframeFunctionTransformer(
            remove_features,
            features=["but_postcode", "zod_idr_zone_dgr"])
         ),
        (
            'cast_str_to_datetime',
            DataframeFunctionTransformer(
                cast_series_to_datetime,
                column_name="day_id"
            )
        ),
        ('create_year_and_week_number', DataframeFunctionTransformer(
            create_year_and_week_column,
            column_name="day_id")
         ),
        (
            'create_df_for_modeling',
            DataframeFunctionTransformer(create_df_for_modeling)
        ),
    ]
