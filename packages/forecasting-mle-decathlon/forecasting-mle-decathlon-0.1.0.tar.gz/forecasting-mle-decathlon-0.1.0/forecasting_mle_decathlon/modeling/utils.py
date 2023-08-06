import pandas as pd
import numpy as np
from vacances_scolaires_france import SchoolHolidayDates


def create_holidays_df(start_year: int, end_year: int) -> pd.DataFrame:
    years = np.arange(start_year, end_year + 1)
    d = SchoolHolidayDates()
    holidays_list = []
    for holiday_year in years:
        holidays_list += list(d.holidays_for_year(holiday_year).keys())
    df = pd.DataFrame(holidays_list, columns=["ds"])
    df["holiday_name"] = "fr_holiday"
    df.rename(columns={"holiday_name": "holiday"}, inplace=True)
    return df
