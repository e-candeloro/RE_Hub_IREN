import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import random
from fbprophet import Prophet
from fbprophet.plot import plot_plotly

# Simulazione dei dati raccolti
def simulate_data():
    types_of_waste = ["Ingombrante", "RAEE", "Organico", "Carta", "Plastica", "Vetro"]
    sources = ["Computer Vision", "App Iren Ambiente", "Chiamata", "Dati Interni"]
    locations = {
        "Centro": (45.0703, 7.6869),
        "Mirafiori": (45.0112, 7.6201),
        "San Salvario": (45.0516, 7.6861),
        "Barriera di Milano": (45.0983, 7.6966),
        "Crocetta": (45.0624, 7.6692),
    }
    start_date = pd.to_datetime("2023-01-01")
    end_date = pd.to_datetime("2023-12-31")
    num_records = 500

    data = []
    for _ in range(num_records):
        date = start_date + pd.to_timedelta(random.randint(0, 364), unit="d")
        location = random.choice(list(locations.keys()))
        data.append({
            "Data": date,
            "Tipo di Rifiuto": random.choice(types_of_waste),
            "Fonte": random.choice(sources),
            "Localizzazione": location,
            "Latitudine": locations[location][0],
            "Longitudine": locations[location][1],
            "Quantità": random.randint(1, 50),
        })

    return pd.DataFrame(data)

# Genera dati simulati
df_collected = simulate_data()

# Previsione con Prophet
def forecast_data(data, periods=30):
    # Aggrega i dati per Data
    df_forecast = data.groupby("Data").sum()["Quantità"].reset_index()
    df_forecast.columns = ["ds", "y"]

    # Modello Prophet
    model = Prophet()
    model.fit(df_forecast)
    
    # Genera previsioni
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    forecast = forecast[["ds", "yhat"]]
    forecast.columns = ["Data", "Quantità"]

    # Aggiungi colonne dummy per Tipo di Rifiuto e Fonte
    forecast["Tipo di Rifiuto"] = "Previsione"
    forecast["Fonte"] = "AI"
    forecast["Localizzazione"] = "Previsione"
    forecast["Latitudine"] = None
    forecast["Longitudine"] = None
    
    return forecast

# Dati previsti
df_forecast = forecast_data(df_collected)

# Creazione dell'app Dash
app = dash.Dash(__name__)
app.title = "Dashboard Rifiuti Torino"

# Layout della dashboard
app.layout = html.Div([
    html.H1("Monitoraggio Rifiuti - Torino", style={"text-align": "center"}),

    # Selettore modalità
    html.Div([
        html.Label("Visualizzazione:"),
        dcc.RadioItems(
            id="mode-selector",
            options=[
                {"label": "Dati Raccolti", "value": "collected"},
                {"label": "Dati Previsti", "value": "forecast"}
            ],
            value="collected",
            inline=True
        ),
    ], style={"text-align": "center", "margin-bottom": "20px"}),

    # Filtri
    html.Div([
        html.Label("Periodo:"),
        dcc.DatePickerRange(
            id="date-filter",
            start_date=df_collected["Data"].min(),
            end_date=df_collected["Data"].max(),
            display_format="YYYY-MM-DD",
        ),
        html.Label("Tipo di Rifiuto:"),
        dcc.Dropdown(
            id="waste-filter",
            options=[{"label": t, "value": t} for t in df_collected["Tipo di Rifiuto"].unique()] + 
                     [{"label": "Previsione", "value": "Previsione"}],
            multi=True,
            placeholder="Seleziona tipo di rifiuto"
        ),
        html.Label("Fonte:"),
        dcc.Dropdown(
            id="source-filter",
            options=[{"label": s, "value": s} for s in df_collected["Fonte"].unique()] + 
                     [{"label": "AI", "value": "AI"}],
            multi=True,
            placeholder="Seleziona fonte"
        ),
    ], style={"width": "30%", "display": "inline-block", "vertical-align": "top"}),

    # Mappa
    html.Div([
        dcc.Graph(id="map-graph")
    ], style={"width": "65%", "display": "inline-block", "padding-left": "5%"}),
])

# Callback per aggiornare la mappa
@app.callback(
    Output("map-graph", "figure"),
    Input("mode-selector", "value"),
    Input("date-filter", "start_date"),
    Input("date-filter", "end_date"),
    Input("waste-filter", "value"),
    Input("source-filter", "value")
)
def update_map(mode, start_date, end_date, selected_waste, selected_sources):
    # Selezione dataset
    data = df_collected if mode == "collected" else df_forecast

    # Filtraggio dei dati
    filtered_df = data[
        (data["Data"] >= pd.to_datetime(start_date)) &
        (data["Data"] <= pd.to_datetime(end_date))
    ]
    if selected_waste:
        filtered_df = filtered_df[filtered_df["Tipo di Rifiuto"].isin(selected_waste)]
    if selected_sources:
        filtered_df = filtered_df[filtered_df["Fonte"].isin(selected_sources)]

    # Creazione della mappa
    fig = px.scatter_mapbox(
        filtered_df,
        lat="Latitudine",
        lon="Longitudine",
        size="Quantità",
        color="Tipo di Rifiuto",
        hover_name="Localizzazione",
        hover_data={"Data": True, "Fonte": True, "Quantità": True},
        zoom=12,
        mapbox_style="carto-positron",
        title="Distribuzione dei Rifiuti"
    )
    return fig

# Esecuzione dell'app
if __name__ == "__main__":
    app.run_server(debug=True)
