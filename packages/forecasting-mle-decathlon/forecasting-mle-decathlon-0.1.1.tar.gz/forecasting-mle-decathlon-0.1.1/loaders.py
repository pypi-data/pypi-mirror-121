import pandas as pd


def load_gz_csv_to_df(filepath: str) -> pd.DataFrame:
    try:
        return pd.read_csv(
            filepath,
            compression='gzip',
            header=0, sep=',',
            error_bad_lines=False
        )
    except FileNotFoundError:
        exit(1)
