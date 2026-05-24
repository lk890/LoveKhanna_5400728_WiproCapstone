import pandas as pd


def get_test_data():

    file = "test_data/product.xlsx"

    return pd.read_excel(file)