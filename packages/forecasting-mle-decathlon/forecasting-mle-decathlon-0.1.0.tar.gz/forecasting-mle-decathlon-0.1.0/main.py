from loaders import load_gz_csv_to_df
from forecasting_mle_decathlon.processing.processing_pipeline import (
    create_processing_pipeline
)
from forecasting_mle_decathlon.modeling.modeling_pipeline import (
    create_modeling_pipeline
)
from forecasting_mle_decathlon.modeling.utils import create_holidays_df
from sklearn.pipeline import Pipeline

import warnings
warnings.simplefilter("ignore")


if __name__ == '__main__':
    bu_df = load_gz_csv_to_df('data/bu_feat.csv.gz')
    train_df = load_gz_csv_to_df('data/train.csv.gz')
    test_df = load_gz_csv_to_df('data/train.csv.gz')

    holidays_df = create_holidays_df(2012, 2017)

    processing_pipeline = create_processing_pipeline(bu_df=bu_df)
    modeling_pipeline = create_modeling_pipeline(holidays_df=holidays_df)
    stages = processing_pipeline + modeling_pipeline
    pipe = Pipeline(stages)

    # FIXME: to remove it's just for test on two bu and dpt
    train_df_two_bu_dpt = train_df[
        (
            (train_df.but_num_business_unit == 64) |
            (train_df.but_num_business_unit == 119)
        ) &
        (train_df.dpt_num_department == 127)
        ]

    models = pipe.fit(train_df_two_bu_dpt)

    predictions = models.predict(X=train_df_two_bu_dpt)
