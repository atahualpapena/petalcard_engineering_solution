import os
import csv
import pandas as pd

file = open('summary.csv', 'a')
pd.set_option("display.precision", 2)
file.write("user_id,n,sum,min,max \n")
for csvfile in os.listdir("data"):
    df = pd.read_csv("data/" + csvfile, sep="|", escapechar="\\")

    def sum_credit_debit(x):
        credit = x[x["type"] == "credit"]["amount"].sum()
        debit = x[x["type"] == "debit"]["amount"].sum()
        return credit - debit

    def calculate_final_amount(x):
        sum = sum_credit_debit(x)
        per_date = x.groupby("date").apply(sum_credit_debit)
        balance_per_date = per_date.cumsum()
        return pd.Series(
            {
                "sum": sum,
                "n": len(x),
                "min": balance_per_date.min(),
                "max": balance_per_date.max(),
            }
        )

    group_df = df.groupby("user_id", as_index=False).apply(calculate_final_amount)

    for index, row in group_df.iterrows():
        row = f'{int(row["user_id"])},{int(row["n"])},{"{:.{}f}".format(row["sum"], 2)},{"{:.{}f}".format(row["min"], 2)},{"{:.{}f}".format(row["max"], 2)}'  # noqa
        file.write(row + "\n")
file.close()