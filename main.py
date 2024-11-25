import dash
from dash import dcc, html, Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Simulazione dati sintetici


def generate_synthetic_data():
    np.random.seed(42)
    locations = ["Centro", "San Salvario", "Crocetta", "Lingotto", "Mirafiori"]
    waste_types = ["Indifferenziato", "Plastica",
                   "Carta", "RAEE", "Ingombranti"]
    sources = ["Visione Computer", "App Iren",
               "Chiamata Cittadini", "Dati Interni"]

    data = pd.DataFrame({
        "location": np.random.choice(locations, 500),
        "date_time": pd.date_range(start="2024-01-01", periods=500, freq="h"),
        "waste_type": np.random.choice(waste_types, 500),
        "source": np.random.choice(sources, 500),
        "quantity": np.random.randint(1, 100, 500),
    })
    return data

# Funzione per previsione


def generate_predictions(days_ahead=1):
    data = generate_synthetic_data()
    data["hour"] = data["date_time"].dt.hour
    data["day"] = data["date_time"].dt.day
    data["month"] = data["date_time"].dt.month

    le_location = LabelEncoder()
    le_waste = LabelEncoder()
    data["location_encoded"] = le_location.fit_transform(data["location"])
    data["waste_type_encoded"] = le_waste.fit_transform(data["waste_type"])

    X = data[["location_encoded", "hour", "day", "month", "quantity"]]
    y = data["waste_type_encoded"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    future_hours = pd.date_range(
        start=data["date_time"].max(), periods=days_ahead * 24, freq="h"
    )
    future_data = pd.DataFrame({
        "date_time": future_hours,
        "location_encoded": np.random.choice(X["location_encoded"].unique(), len(future_hours)),
        "hour": future_hours.hour,
        "day": future_hours.day,
        "month": future_hours.month,
        "quantity": np.random.randint(1, 100, len(future_hours)),
    })
    future_data["waste_type_encoded"] = model.predict(
        future_data[["location_encoded", "hour", "day", "month", "quantity"]])
    future_data["waste_type"] = future_data["waste_type_encoded"].round().astype(
        int).map(dict(enumerate(data["waste_type"].unique())))
    future_data["location"] = future_data["location_encoded"].map(
        dict(enumerate(data["location"].unique())))
    return future_data


# Creazione app Dash
app = dash.Dash(__name__)
app.title = "eye-REN"  # Titolo cambiato

# Layout della dashboard
app.layout = html.Div(style={'backgroundColor': '#FFFFFF', 'padding': '20px'}, children=[
    # Link per il font Poppins
    html.Link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap"
    ),

    html.H1("eye-REN", style={  # Titolo aggiornato
        "textAlign": "center",
        "marginBottom": "40px",  # Aggiunto più spazio sotto il titolo
        'color': '#03A64A',  # Verde per i titoli
        'fontFamily': 'Poppins, sans-serif'
    }),

    html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'}, children=[
        # Sezione filtri
        html.Div(style={'width': '100%', 'maxWidth': '25%', 'backgroundColor': '#F1F1F1', 'padding': '20px', 'borderRadius': '8px', 'marginBottom': '20px'}, children=[
            html.H3("Filtri Dati Raccolti", style={
                    'color': '#03A64A', 'fontFamily': 'Poppins, sans-serif'}),
            dcc.Dropdown(
                id="filter-waste",
                options=[{"label": wt, "value": wt}
                         for wt in generate_synthetic_data()["waste_type"].unique()],
                multi=True,
                placeholder="Seleziona il tipo di rifiuto",
                style={'marginBottom': '20px'}
            ),
            dcc.Dropdown(
                id="filter-source",
                options=[{"label": src, "value": src}
                         for src in generate_synthetic_data()["source"].unique()],
                multi=True,
                placeholder="Seleziona la fonte",
                style={'marginBottom': '20px'}
            ),
            dcc.DatePickerRange(
                id="filter-date",
                start_date="2024-01-01",
                end_date="2024-01-31",
                display_format="YYYY-MM-DD",
                style={"marginTop": "10px", "marginBottom": "20px"}
            ),
        ]),

        # Sezione mappa dati raccolti
        html.Div(style={'width': '100%', 'maxWidth': '65%', 'backgroundColor': '#F1F1F1', 'padding': '20px', 'borderRadius': '8px'}, children=[
            dcc.Graph(id="map-collected"),
        ])
    ]),

    # Divisore verde
    html.Hr(style={'borderColor': '#03A64A', 'borderWidth': '2px'}),

    html.Div(style={'backgroundColor': '#F1F1F1', 'padding': '20px', 'borderRadius': '8px'}, children=[
        html.H3("Previsioni", style={
                'color': '#03A64A', 'fontFamily': 'Poppins, sans-serif'}),
        html.Div([
            dcc.Input(
                id="prediction-days",
                type="number",
                placeholder="Giorni di previsione (default: 1)",
                style={"marginBottom": "10px"}
            ),
            html.Button("Aggiorna Previsioni",
                        id="update-predictions", n_clicks=0),
        ], style={"marginBottom": "20px"}),
        dcc.Graph(id="map-predicted"),
    ])
])

# Callback per mappa dati raccolti


@app.callback(
    Output("map-collected", "figure"),
    [Input("filter-waste", "value"),
     Input("filter-source", "value"),
     Input("filter-date", "start_date"),
     Input("filter-date", "end_date")]
)
def update_collected_map(selected_waste, selected_source, start_date, end_date):
    data = generate_synthetic_data()

    # Filtro per tipo di rifiuto
    if selected_waste:
        data = data[data["waste_type"].isin(selected_waste)]

    # Filtro per fonte
    if selected_source:
        data = data[data["source"].isin(selected_source)]

    # Filtro per intervallo di date
    data["date_time"] = pd.to_datetime(data["date_time"])
    data = data[(data["date_time"] >= start_date)
                & (data["date_time"] <= end_date)]

    if data.empty:
        return px.scatter_mapbox(
            title="Nessun dato disponibile",
            mapbox_style="carto-positron",
            zoom=10
        )

    data["count"] = 1
    fig = px.scatter_mapbox(
        data,
        lat=np.random.uniform(45.05, 45.10, len(data)),
        lon=np.random.uniform(7.60, 7.70, len(data)),
        color="waste_type",
        size="quantity",
        hover_name="location",
        mapbox_style="carto-positron",
        zoom=12,
        title="Distribuzione Rifiuti Raccolti",
        color_continuous_scale="Viridis"
    )
    fig.update_layout(
        # Colore nero per il testo del titolo
        title_font=dict(family="Poppins", size=20, color='#211A1D'),
        # Colore nero per il testo delle etichette
        font=dict(family="Poppins", size=12, color='#211A1D')
    )
    return fig

# Callback per previsioni


@app.callback(
    Output("map-predicted", "figure"),
    [Input("prediction-days", "value")]
)
def update_prediction_map(days_ahead):
    days_ahead = int(days_ahead) if days_ahead else 1
    predicted_data = generate_predictions(days_ahead)

    fig = px.scatter_mapbox(
        predicted_data,
        lat=np.random.uniform(45.05, 45.10, len(predicted_data)),
        lon=np.random.uniform(7.60, 7.70, len(predicted_data)),
        color="waste_type",
        size="quantity",
        hover_name="location",
        mapbox_style="carto-positron",
        zoom=12,
        title="Distribuzione Rifiuti Previsti",
        color_continuous_scale="Viridis"
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
