import pandas as pd
from forecasting.modeling.prophet_estimator import ProphetEstimator
from typing import List, Tuple


def create_modeling_pipeline(
        holidays_df: pd.DataFrame
) -> List[Tuple[str, ProphetEstimator]]:
    return [
        ('model', ProphetEstimator(holidays_df))
    ]
