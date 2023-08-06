class DataframeFunctionTransformer():
    """
    Generic class to create custom estimator/transformer
    """
    def __init__(self, func, **kwargs):
        self.func = func
        self.parameters = kwargs

    def transform(self, input_df):
        return self.func(input_df, **self.parameters)

    def fit(self, X, y=None, **fit_params):
        return self
