# Final Assignment: Part 2 - Create Dashboard with Plotly and Dash
# Automobile Sales Statistics Dashboard
#
# Tasks covered:
# 2.1 - Create Dash application and meaningful title
# 2.2 - Add dropdown menus
# 2.3 - Add output container
# 2.4 - Create callbacks
# 2.5 - Create graphs for Recession Period Statistics
# 2.6 - Create graphs for Yearly Statistics

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


# ---------------------------------------------------------------------------
# Load the historical automobile sales data
# ---------------------------------------------------------------------------
DATA_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/"
    "historical_automobile_sales.csv"
)

data = pd.read_csv(DATA_URL)


# ---------------------------------------------------------------------------
# TASK 2.1 - Initialize Dash application and give it a meaningful title
# ---------------------------------------------------------------------------
app = dash.Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"


# ---------------------------------------------------------------------------
# TASK 2.2 - Create dropdown menu options
# ---------------------------------------------------------------------------
dropdown_options = [
    {"label": "Yearly Statistics", "value": "Yearly Statistics"},
    {
        "label": "Recession Period Statistics",
        "value": "Recession Period Statistics",
    },
]

# Years available in the assignment dataset
year_list = sorted(data["Year"].dropna().unique().tolist())


# ---------------------------------------------------------------------------
# TASK 2.2 / TASK 2.3 - Dashboard layout
# ---------------------------------------------------------------------------
app.layout = html.Div(
    [
        html.H1(
            "Automobile Sales Statistics Dashboard",
            style={
                "textAlign": "center",
                "color": "#503D36",
                "fontSize": 24,
            },
        ),

        html.Div(
            [
                html.Label("Select Statistics:"),

                dcc.Dropdown(
                    id="dropdown-statistics",
                    options=dropdown_options,
                    placeholder="Select a report type",
                    value="Select Statistics",
                    style={
                        "width": "80%",
                        "padding": "3px",
                        "fontSize": 20,
                        "textAlignLast": "center",
                    },
                ),
            ]
        ),

        html.Br(),

        html.Div(
            [
                html.Label("Select Year:"),
                dcc.Dropdown(
                    id="select-year",
                    options=[
                        {"label": int(year), "value": int(year)}
                        for year in year_list
                    ],
                    placeholder="Select a year",
                    style={
                        "width": "80%",
                        "padding": "3px",
                        "fontSize": 20,
                        "textAlignLast": "center",
                    },
                ),
            ]
        ),

        html.Br(),

        html.Div(
            id="output-container",
            className="chart-grid",
            style={
                "display": "flex",
                "flexDirection": "column",
            },
        ),
    ]
)


# ---------------------------------------------------------------------------
# TASK 2.4 - Callback to enable/disable the year dropdown
# ---------------------------------------------------------------------------
@app.callback(
    Output(component_id="select-year", component_property="disabled"),
    Input(component_id="dropdown-statistics", component_property="value"),
)
def update_input_container(selected_statistics):
    """
    Disable the year dropdown for Recession Period Statistics.
    Enable the year dropdown for Yearly Statistics.
    """
    if selected_statistics == "Yearly Statistics":
        return False
    else:
        return True


# ---------------------------------------------------------------------------
# TASK 2.4 / TASK 2.5 / TASK 2.6
# Callback to create and display the dashboard graphs
# ---------------------------------------------------------------------------
@app.callback(
    Output(
        component_id="output-container",
        component_property="children",
    ),
    [
        Input(
            component_id="dropdown-statistics",
            component_property="value",
        ),
        Input(
            component_id="select-year",
            component_property="value",
        ),
    ],
)
def update_output_container(selected_statistics, selected_year):

    # =======================================================================
    # TASK 2.5 - Recession Period Statistics
    # =======================================================================
    if selected_statistics == "Recession Period Statistics":

        recession_data = data[data["Recession"] == 1]

        # -------------------------------------------------------------------
        # Recession Plot 1:
        # Average automobile sales fluctuation over the recession period
        # -------------------------------------------------------------------
        yearly_rec = (
            recession_data.groupby("Year")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x="Year",
                y="Automobile_Sales",
                title=(
                    "Average Automobile Sales Fluctuation "
                    "Over Recession Period"
                ),
            )
        )

        # -------------------------------------------------------------------
        # Recession Plot 2:
        # Average vehicles sold by vehicle type
        # -------------------------------------------------------------------
        avg_vehicles_sold = (
            recession_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        R_chart2 = dcc.Graph(
            figure=px.bar(
                avg_vehicles_sold,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title=(
                    "Average Number of Vehicles Sold by Vehicle Type "
                    "During Recession"
                ),
            )
        )

        # -------------------------------------------------------------------
        # Recession Plot 3:
        # Advertising expenditure share by vehicle type
        # -------------------------------------------------------------------
        exp_rec = (
            recession_data.groupby("Vehicle_Type")[
                "Advertising_Expenditure"
            ]
            .sum()
            .reset_index()
        )

        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title=(
                    "Total Expenditure Share by Vehicle Type "
                    "During Recession"
                ),
            )
        )

        # -------------------------------------------------------------------
        # Recession Plot 4:
        # Effect of unemployment rate on vehicle type and sales
        # -------------------------------------------------------------------
        unemployment_effect = (
            recession_data.groupby(
                ["Vehicle_Type", "unemployment_rate"]
            )["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemployment_effect,
                x="Vehicle_Type",
                y="Automobile_Sales",
                color="unemployment_rate",
                title=(
                    "Effect of Unemployment Rate on Vehicle Type "
                    "and Sales During Recession"
                ),
            )
        )

        return [
            html.Div(
                children=[R_chart1, R_chart2],
                style={
                    "display": "flex",
                    "width": "100%",
                },
            ),
            html.Div(
                children=[R_chart3, R_chart4],
                style={
                    "display": "flex",
                    "width": "100%",
                },
            ),
        ]

    # =======================================================================
    # TASK 2.6 - Yearly Statistics
    # =======================================================================
    elif (
        selected_statistics == "Yearly Statistics"
        and selected_year is not None
    ):

        yearly_data = data[data["Year"] == selected_year]

        # -------------------------------------------------------------------
        # Yearly Plot 1:
        # Average automobile sales for the whole period
        # -------------------------------------------------------------------
        yas = (
            data.groupby("Year")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x="Year",
                y="Automobile_Sales",
                title="Yearly Automobile Sales",
            )
        )

        # -------------------------------------------------------------------
        # Yearly Plot 2:
        # Total monthly automobile sales for selected year
        # -------------------------------------------------------------------
        monthly_sales = (
            yearly_data.groupby("Month")["Automobile_Sales"]
            .sum()
            .reset_index()
        )

        Y_chart2 = dcc.Graph(
            figure=px.line(
                monthly_sales,
                x="Month",
                y="Automobile_Sales",
                title=(
                    f"Total Monthly Automobile Sales in {selected_year}"
                ),
            )
        )

        # -------------------------------------------------------------------
        # Yearly Plot 3:
        # Average vehicles sold by vehicle type
        # -------------------------------------------------------------------
        avr_vdata = (
            yearly_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title=(
                    f"Average Vehicles Sold by Vehicle Type "
                    f"in {selected_year}"
                ),
            )
        )

        # -------------------------------------------------------------------
        # Yearly Plot 4:
        # Total advertisement expenditure for each vehicle type
        # -------------------------------------------------------------------
        exp_data = (
            yearly_data.groupby("Vehicle_Type")[
                "Advertising_Expenditure"
            ]
            .sum()
            .reset_index()
        )

        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title=(
                    "Total Advertisement Expenditure "
                    "for Each Vehicle Type"
                ),
            )
        )

        return [
            html.Div(
                children=[Y_chart1, Y_chart2],
                style={
                    "display": "flex",
                    "width": "100%",
                },
            ),
            html.Div(
                children=[Y_chart3, Y_chart4],
                style={
                    "display": "flex",
                    "width": "100%",
                },
            ),
        ]

    # No report selected yet
    return None


# ---------------------------------------------------------------------------
# Run the Dash application
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
