# %%
import pandas as pd

df = pd.read_csv(
    "https://d14wlfuexuxgcm.cloudfront.net/covid/rt.csv",
    usecols=["date", "region", "mean"],
    parse_dates=["date"],
    infer_datetime_format=True,
)

case_data = pd.read_csv(
    "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv",
    parse_dates=["date"],
    infer_datetime_format=True,
    usecols=["date", "state", "cases", "deaths"],
)

# %%
test = pd.read_csv("data/rt.csv")

latest = sorted(df["date"].unique())[-1]
latest_cases = sorted(case_data["date"].unique())[-1]

if latest_cases != latest:
    return f"No run: NYT data ({latest_cases}) and RT data ({latest}) are different."

    on_file = sorted(test["date"].unique())[-1]

elif latest == on_file:
    print("No run")
else:
    print(f"Run: On file is {on_file}, latest is {latest}")
    get_ipython().system("./run.sh")
