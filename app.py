import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
from collections import Counter
import plotly.express as px


endpoint_url = 'http://127.0.0.1:9008/dashboard/gifts/?format=json'

data = pd.read_json(endpoint_url)
packages = data.giftname.unique()

data["Date"] = pd.to_datetime(data["gifted_at"], format="%Y-%m-%d")
count_arr = Counter(data['usname'])
usernames = count_arr.keys()
giftcounts = []
for d in count_arr.values():
    giftcounts.append(d)

data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        'https://codepen.io/chriddyp/pen/bWLwgP.css'
    },
]
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Gifts Analytics"
usernames = data.usname.unique()
dates = data.Date.unique()
print(dates)
df = pd.DataFrame(
    {
    "user":usernames,
    "giftcount":giftcounts,

    }
)

#fig = px.bar(df,x="user",y="giftcount",color="user",barmode="relative")

app.layout = html.Div(
    children=[
     html.Div(
            children=[
                # html.P(children="Gifts", className="header-emoji"),
                html.H1(
                    children="Gifts Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze champ Gifts to clients",
                    className="header-description",
                ),
            ],
            className="header",
        ),
    html.Div(children=[
        html.Div(
            children="Select Date",
            className="menu-title"
        ),
        dcc.DatePickerRange(
            id="date-range",
            min_date_allowed=data.Date.min().date(),
            max_date_allowed = data.Date.max().date(),
            start_date = data.Date.min().date(),
            end_date = data.Date.max().date()

        ),
    ],
    className="menu"
    ),

    html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="analytics-graph", config={"displayModeBar": False},relayoutData= {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

#try define callbacks here
@app.callback(
    [Output("analytics-graph","figure")],
    [
        Input("date-range","start_date"),
        Input("date-range","end_date"),

    ],
)

def update_charts(start_date,end_date):
    data = pd.read_json(endpoint_url)
    data["Date"] = pd.to_datetime(data["gifted_at"], format="%Y-%m-%d")
    mask = (
        (data.Date >= start_date)
        & (data.Date <= end_date)
    )
    print(data.Date.max().date())
    filtered_data = data.loc[mask, :]
    count_arr = Counter(filtered_data['usname'])
    usernames = count_arr.keys()
    giftcounts = []
    for d in count_arr.values():
        giftcounts.append(d)
    usernames = list(filtered_data.usname.unique())
    print(giftcounts)
    print(usernames)
    df = pd.DataFrame(
        {
        "user":usernames,
        "giftcount":giftcounts,

        })

    #fig = px.bar(df,x="user",y="giftcount",color="user",barmode="relative")
    analytics_chart_figure = {
        "data": [
            {
                "x": usernames,
                "y": giftcounts,
                "type":"lines"

            },

        ],


        "layout": {
            "title": {
                "text": "Gift Count per Champ",
                "x": 0.05,
                "xanchor": "left",

            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "", "fixedrange": True},
            "colorway": ["#17B897"],

        },

    }

    return [analytics_chart_figure]


if __name__ == "__main__":
    app.run_server(debug=True)
