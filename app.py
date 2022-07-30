
from datetime import date
import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Output, Input

data = pd.read_csv("532175.csv")
data = data.iloc[:,:8]


data["Date"] = pd.to_datetime(data["Date"])

data.sort_values("Date", inplace=True)


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "CYIENT Stock Analytics:!"


app.layout = html.Div(
    
    children=
    [
        html.Div(html.Img(src="assets\Cyient-Ltd-Logo.png", className="header-img", width= 100,),),
        html.H1(children="CYIENT Stock Analytics",className="header-title"),
        html.P(
            children="Analyze the behavior of cyient stock prices"
            " and the number of shares traded till now"
            " between 1991 and 2022",
            className="header-description",
        ),
        
        
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            
                            

                            start_date="01-04-2022",
                            end_date=data.Date.max().date()
                           ),
                         ]
                       ),
                      ],
                   className="menu",
                ),

            html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="open-chart", config={"displayModeBar": True},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="close-chart", config={"displayModeBar": True},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="share-chart", config={"displayModeBar": True},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
           )

    ],
    className="header",
)


@app.callback(
    [Output("open-chart", "figure"), Output("close-chart", "figure"), Output("share-chart", "figure")],
    [
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts( start_date, end_date):
    mask = (
        (data.Date >= start_date)
        & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]
    open_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Open Price"],
                "type": "lines",
                "hovertemplate": "%{x}, ₹%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Open Price of CYIENT",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "₹", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    close_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["Close Price"],
                "type": "lines",
                "hovertemplate": "%{x}, ₹%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {"text": "Close Price of CYIENT", 
                "x": 0.05, 
                "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "₹", "fixedrange": True},
            "colorway": ["#E12D39"],
                  },
    }

    share_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data["No.of Shares"],
                "type": "lines",
                
            },
        ],
        "layout": {
            "title": {"text": "Number of Shares Traded of CYIENT", 
                "x": 0.05, 
                "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "", "fixedrange": True},
            "colorway": ["#E12D39"],
        },
       }
    
    return open_chart_figure, close_chart_figure, share_chart_figure



if __name__ == "__main__":
    app.run_server(debug=True)

