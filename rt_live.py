# -*- coding: utf-8 -*-
# %%
import datetime as dt
import functools
import json
from urllib.request import urlopen

# import ipywidgets as widgets
import numpy as np
import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt

# %%
df = pd.read_csv(
    "https://d14wlfuexuxgcm.cloudfront.net/covid/rt.csv",
    usecols=["date", "region", "mean"],
    parse_dates=["date"],
    infer_datetime_format=True,
)

# %%
df.columns = ["date", "STUSPS", "rt"]

# %%
df["rt"] = round(df.rt, 2)

# %%
url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"

# %%
with urlopen(url) as response:
    us = json.load(response)


# %%
state_id = []
STUSPS = []
state_name = []

for state in list(range(0, 51)):
    print(us.get("features")[state].get("id"))
    state_id.append(us.get("features")[state].get("id"))
    state_name.append((us.get("features")[state]).get("properties").get("name"))
    print((us.get("features")[state]).get("properties").get("name"))

# %%
abbre = {
    "AK": "Alaska",
    "AL": "Alabama",
    "AR": "Arkansas",
    "AZ": "Arizona",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DC": "District of Columbia",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "IA": "Iowa",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "MA": "Massachusetts",
    "MD": "Maryland",
    "ME": "Maine",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "NE": "Nebraska",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NV": "Nevada",
    "NY": "New York",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VA": "Virginia",
    "VT": "Vermont",
    "WA": "Washington",
    "WI": "Wisconsin",
    "WV": "West Virginia",
    "WY": "Wyoming",
}

# %%
print(state_name)

# %%
state_codes = dict(zip(abbre, state_id))

# %%
state_codes

# %%
state_name = dict(zip(abbre, state_name))

# %%
df["state"] = df["STUSPS"].map(state_name)

# %%
df["state_id"] = df["STUSPS"].map(state_codes)

# %%
df

# %%
df.query("STUSPS == 'CA'").query("date == '2020-11-04'")

# %%
latest = sorted(df["date"].unique())[-1]
two_w_ago = latest - np.timedelta64(14, "D")
one_m_ago = (pd.Timestamp(latest) - pd.DateOffset(months=1)).to_numpy()
two_m_ago = (pd.Timestamp(latest) - pd.DateOffset(months=2)).to_numpy()
three_m_ago = (pd.Timestamp(latest) - pd.DateOffset(months=3)).to_numpy()

# %%
dates = [latest, two_w_ago, one_m_ago, two_m_ago, three_m_ago]

# %%
date_ranges = [df["date"] == date for date in dates]


# %%
date_ranges = functools.reduce(lambda x, y: x | y, date_ranges)

# %%
plotly = df[date_ranges]

# %%
plotly.sort_values(by=["date"], inplace=True, ascending=True)

# %%
plotly.to_csv("data/rt.csv", index=False)

# %%
plotly = pd.read_csv("data/rt.csv", dtype={"state_id": str})

# %%
# fig = px.choropleth_mapbox(
fig = px.choropleth(
    plotly,
    geojson=us,
    locations="state_id",
    featureidkey="id",
    animation_frame="date",
    animation_group="rt",
    color="rt",
    color_continuous_scale=[
        (0, "green"),
        (0.5, "rgb(135, 226, 135)"),
        (0.5, "rgb(226, 136, 136)"),
        (1, "red"),
    ],
    hover_name="state",
    hover_data=["date", "state", "rt"],
    range_color=(0, 2),
    center={"lon": -94.99141861526407, "lat": 38.1354813882185},
    #     zoom=2.3350828189345934,
    #     mapbox_style="carto-positron",
    scope="usa",
    labels={"date": "Date", "state": "State", "rt": "Rₜ"},
)


fig.layout.font.family = "Arial"

# fig.update_geos(fitbounds="locations", visible=False)

fig.update_layout(
    width=1000,
    height=1000,
    title=f"Rₜ: COVID-19 | United States",
    annotations=[
        dict(
            xanchor="right",
            x=1,
            yanchor="top",
            y=-0.05,
            showarrow=False,
            text="Sources: rt.live, U.S. Census Bureau",
        )
    ],
    autosize=True,
)

fig.show()

# %%
with open("../danielcs88.github.io/html/rt_live.html", "w") as f:
    f.write(fig.to_html(include_plotlyjs="cdn"))


# %%
get_ipython().system(" cd ../danielcs88.github.io/ && git pull")


# %%
get_ipython().system(
    ' cd ../danielcs88.github.io/ && git add --all && git commit -m "Update" && git push'
)
