import sqlite3
import networkx as nx
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
from itertools import combinations

# Connect to the SQLite database and fetch movie-actor data
db_path = "data/rotten_tomatoes.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT movie_id, movie_title, actor_in_info FROM main_actors_in_info")
data = cursor.fetchall()
conn.close()

# Create an empty graph
G = nx.Graph()

# Group actors by movie_id and movie_title
movies = {}
for movie_id, movie_title, actor in data:
    if movie_id not in movies:
        movies[movie_id] = {"actors": set(), "title": movie_title}  # Store actors and movie title
    movies[movie_id]["actors"].add(actor)

# Add edges for actors who share the same movie_id and store movie titles in edge attributes
for movie_id, movie_info in movies.items():
    actors = movie_info["actors"]
    movie_title = movie_info["title"]
    for actor1, actor2 in combinations(actors, 2):
        if G.has_edge(actor1, actor2):
            G[actor1][actor2]['movies'].append(movie_title)  # Append movie title if edge already exists
        else:
            G.add_edge(actor1, actor2, movies=[movie_title])  # Create edge with initial movie title

# Prepare graph layout and traces
pos = nx.spring_layout(G, k=0.25, iterations=50)
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'),
                        hoverinfo='none', mode='lines')

node_x = []
node_y = []
node_text = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(node)

node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text', text=node_text,
                        marker=dict(size=10, color='LightSkyBlue'), hoverinfo='text')

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(title="Actor Co-occurrence Network", showlegend=False,
                                 hovermode='closest', margin=dict(b=0, l=0, r=0, t=40),
                                 width=1450, height=700,  # Aukið breidd og hæð
                                 xaxis=dict(showgrid=False, zeroline=False),
                                 yaxis=dict(showgrid=False, zeroline=False)))


# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="network-graph", figure=fig),
    html.Div(id="output-text", style={'font-size': '20px', 'margin-top': '20px'})
])

# Store the selected nodes
selected_nodes = []

@app.callback(
    Output("output-text", "children"),
    [Input("network-graph", "clickData")]
)
def display_connection(clickData):
    global selected_nodes
    if clickData:
        clicked_node = clickData['points'][0]['text']
        selected_nodes.append(clicked_node)

        # Keep only the last two nodes clicked
        if len(selected_nodes) > 2:
            selected_nodes.pop(0)

        # If two nodes are selected, check for shared movies
        if len(selected_nodes) == 2:
            actor1, actor2 = selected_nodes
            if G.has_edge(actor1, actor2):
                movies_shared = G[actor1][actor2]['movies']
                selected_nodes = []  # Reset after displaying the result
                return f"{actor1} and {actor2} played together in: " + ", ".join(movies_shared)
            else:
                selected_nodes = []
                return f"{actor1} and {actor2} have not starred in a movie together."

    return "Click on two actor nodes to see their shared movies."

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True, port=8063)
