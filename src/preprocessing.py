import pandas as pd


def convert_dates(df):
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df


def count_missing_values(df):
    return df.isnull().sum().sum()


def count_duplicate_rows(df):
    return df.duplicated().sum()