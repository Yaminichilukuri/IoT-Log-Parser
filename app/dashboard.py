from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px

app = Dash(__name__)

# Load structured data
data_file = "../data/structured_data.csv"
df = pd.read_csv(data_file)

# Create a temperature chart
if "Temperature" in df.columns:
    fig = px.line(df, y="Temperature", title="Temperature Over Time")

app.layout = html.Div([
    html.H1("IoT Data Dashboard"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run_server(debug=True)
