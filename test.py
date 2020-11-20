# %%
import pandas as pd

df = pd.read_csv(
    "https://d14wlfuexuxgcm.cloudfront.net/covid/rt.csv",
    usecols=["date", "region", "mean"],
    parse_dates=["date"],
    infer_datetime_format=True,
)

# %%
test = pd.read_csv("data/rt.csv")

latest = sorted(df["date"].unique())[-1]
on_file = sorted(test["date"].unique())[-1]

if latest == on_file:
    print("No run")

else:
    print(f"Run: On file is {on_file}, latest is {latest}")
    get_ipython().system("./run.sh")
