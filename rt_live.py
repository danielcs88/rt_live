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
df.columns = ["date", "state", "rt"]

# %%
df["rt"] = round(df.rt, 2)

# %%
url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"

# %%
# state_id = []
# STUSPS = []
# state_name = []

# for state in list(range(0, 51)):
#     state_id.append(us.get("features")[state].get("id"))
#     state_name.append((us.get("features")[state]).get("properties").get("name"))
#     name = (us.get("features")[state]).get("properties").get("name")
#     #     print(name)
#     code = us.get("features")[state].get("id")
#     print(f"'{name}': '{code}'")

# %%
with urlopen(url) as response:
    us = json.load(response)


# %%
abbre = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
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
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}

# %%
state_codes = {
    "Alabama": "01",
    "Alaska": "02",
    "Arizona": "04",
    "Arkansas": "05",
    "California": "06",
    "Colorado": "08",
    "Connecticut": "09",
    "Delaware": "10",
    "District of Columbia": "11",
    "Florida": "12",
    "Georgia": "13",
    "Hawaii": "15",
    "Idaho": "16",
    "Illinois": "17",
    "Indiana": "18",
    "Iowa": "19",
    "Kansas": "20",
    "Kentucky": "21",
    "Louisiana": "22",
    "Maine": "23",
    "Maryland": "24",
    "Massachusetts": "25",
    "Michigan": "26",
    "Minnesota": "27",
    "Mississippi": "28",
    "Missouri": "29",
    "Montana": "30",
    "Nebraska": "31",
    "Nevada": "32",
    "New Hampshire": "33",
    "New Jersey": "34",
    "New Mexico": "35",
    "New York": "36",
    "North Carolina": "37",
    "North Dakota": "38",
    "Ohio": "39",
    "Oklahoma": "40",
    "Oregon": "41",
    "Pennsylvania": "42",
    "Rhode Island": "44",
    "South Carolina": "45",
    "South Dakota": "46",
    "Tennessee": "47",
    "Texas": "48",
    "Utah": "49",
    "Vermont": "50",
    "Virginia": "51",
    "Washington": "53",
    "West Virginia": "54",
    "Wisconsin": "55",
    "Wyoming": "56",
}

# %%
df["state"] = df["state"].map(abbre)

# %%
df["state_id"] = df["state"].map(state_codes)

# %%
df

# %%
df.query("state == 'CA'").query("date == '2020-11-04'")

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
