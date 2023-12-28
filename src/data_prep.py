import pandas as pd 
import numpy as np

from utils import *


df = pd.read_csv("data/train.csv")

df["Order Date"] = pd.to_datetime(df["Order Date"], format='mixed')
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format='mixed')

df["Duree"] = df["Ship Date"] - df["Order Date"]

df["Duration in days"] = df["Duree"].apply(lambda x: int(str(x).split(" ")[0]))

df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month_name()

df.drop(columns=["Order ID", "Customer ID", "Postal Code", "Product ID"], inplace=True)
df.rename(columns={"Row ID": "id", "Order Date": "Order_date", "Ship Date": "Ship_date", "Ship Mode": "Mode"}, inplace=True)

df['Season'] = df['Month'].map(season_mapping)

df["dayofyear"] = df["Order_date"].dt.dayofyear
df = df[~((df["Order_date"].dt.month == 2) & (df["Order_date"].dt.day == 29))].copy()
df["dayofyear"] = df["dayofyear"].where(
    ~((df["Order_date"].dt.month > 2) & (df["Order_date"].dt.is_leap_year)),
    df["dayofyear"] - 1,
)