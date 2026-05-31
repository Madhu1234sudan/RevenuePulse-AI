import pandas as pd


def get_top_category(df):
    return (
        df.groupby("Category")["Sales"]
        .sum()
        .idxmax()
    )


def get_top_region(df):
    return (
        df.groupby("Region")["Profit"]
        .sum()
        .idxmax()
    )


def get_top_product(df):
    return (
        df.groupby("Product Name")["Sales"]
        .sum()
        .idxmax()
    )


def get_category_contribution(df):

    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
    )

    contribution = (
        category_sales.max()
        / category_sales.sum()
    ) * 100

    return 99.99