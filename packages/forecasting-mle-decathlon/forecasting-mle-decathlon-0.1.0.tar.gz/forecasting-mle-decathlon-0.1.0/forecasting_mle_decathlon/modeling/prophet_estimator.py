from sklearn.base import BaseEstimator
from prophet import Prophet


class ProphetEstimator(BaseEstimator):
    def __init__(self, holidays_df):
        super().__init__()
        self.holidays_df = holidays_df
        self.models = {}

    def fit(self, dfs, Y=None):
        for df in dfs:
            df = df.reset_index(drop=True)
            model = Prophet(
                holidays=self.holidays_df,
                holidays_prior_scale=1
            )
            model.fit(df[["ds", "y"]])
            key = df.loc[0]["but_bu_dpt_id"]
            self.models[key] = model
        return self

    def predict(self, X=None):
        predictions = {}
        for key in self.models.keys():
            future_df = (
                self.models
                    .get(key)
                    .make_future_dataframe(periods=8, freq='W')
            )
            predictions[key] = self.models.get(key).predict(future_df)
        return predictions
