import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Label('Number of observations:'),
        dcc.Slider(
            id='obs',
            min=10,
            max=500,
            value=100,
            marks={str(i): str(i) for i in range(10, 501, 50)},
            step=1
        )
    ], style={'width': '25%', 'display': 'inline-block', 'padding': '20px'}),
    html.Div([
        dcc.Graph(id='distPlot')
    ], style={'width': '70%', 'display': 'inline-block', 'vertical-align': 'top'})
])

@app.callback(
    Output('distPlot', 'figure'),
    [Input('obs', 'value')]
)
def update_figure(obs):
    x = np.random.randn(obs)
    fig = go.Figure(data=[go.Histogram(
        x=x,
        marker=dict(color='darkgray', line=dict(color='white', width=1))
    )])
    fig.update_layout(
        xaxis_title='Value',
        yaxis_title='Frequency',
        bargap=0.2,
        bargroupgap=0.1,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
