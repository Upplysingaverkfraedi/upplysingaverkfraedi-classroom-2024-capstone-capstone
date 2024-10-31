import sqlite3
import pandas as pd
from shiny import App, ui, render
from shinywidgets import output_widget, render_plotly
import plotly.express as px

# Check if the database already exists to avoid overwriting
db_path = 'premier_league.db'
# Load CSV files into DataFrames
games_df = pd.read_csv('Games_season19-20.csv')
player_stats_df = pd.read_csv('Premier League Player Stats.csv')
stadiums_df = pd.read_csv('stadiums-with-GPS-coordinates.csv')

# Create a new SQLite database (or connect to an existing one)
conn = sqlite3.connect(db_path)

# Drop tables if they exist to ensure fresh import
conn.execute("DROP TABLE IF EXISTS Games")
conn.execute("DROP TABLE IF EXISTS PlayerStats")
conn.execute("DROP TABLE IF EXISTS Stadiums")

# Insert the data into the database
games_df.to_sql('Games', conn, if_exists='replace', index=False)
player_stats_df.to_sql('PlayerStats', conn, if_exists='replace', index=False)
stadiums_df.to_sql('Stadiums', conn, if_exists='replace', index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()
print("Database and tables created, and data imported.")

# Load initial data from the database
def load_data_from_db():
    conn = sqlite3.connect(db_path)
    games_df = pd.read_sql_query("SELECT * FROM Games", conn)
    player_stats_df = pd.read_sql_query("SELECT * FROM PlayerStats", conn)
    stadiums_df = pd.read_sql_query("SELECT * FROM Stadiums", conn)
    conn.close()
    return games_df, player_stats_df, stadiums_df

games_df, player_stats_df, stadiums_df = load_data_from_db()

# UI setup with title text
app_ui = ui.page_fluid(
    # Title and navigation bar styling
    ui.tags.head(
        ui.tags.style("""
            h1 { text-align: center; margin-top: 20px; }
            h3 { text-align: center; color: gray; margin-bottom: 20px; }
            .nav-tabs { display: flex; justify-content: center; }
            .nav-tabs .nav-item { margin: 0 10px; }
        """)
    ),
    
    # Title at the top of the page
    ui.tags.div(
        ui.h1("Enska Úrvalsdeildin"),
        ui.h3("2019/20"),
    ),
    
    # Shiny navigation tabs centered below the title
    ui.navset_tab(
        ui.nav_panel(
            "Heim",
            ui.h2("Premier League Home"),
            ui.p("Welcome to the Premier League Analysis.")
        ),
        ui.nav_panel(
            "Stöðutafla",
            ui.h2("League Table"),
            ui.p("League table content goes here.")
        ),
        ui.nav_panel(
            "Stadiums",
            ui.h2("Stadiums with GPS Coordinates"),
            output_widget("stadiums_map"),
            ui.p("Map of stadiums in the Premier League with GPS coordinates.")
        ),
        # Additional placeholder tabs
        ui.nav_panel("x", ui.h2("Placeholder for x")),
        ui.nav_panel("y", ui.h2("Placeholder for y")),
        ui.nav_panel("z", ui.h2("Placeholder for z")),
        ui.nav_panel("d", ui.h2("Placeholder for d")),
    ),
    title="Premier League Analysis"
)

# Server logic
def server(input, output, session):
    # Stadiums map with GPS coordinates
    @output
    @render_plotly
    def stadiums_map():
        fig = px.scatter_mapbox(
            stadiums_df,
            lat="Latitude",
            lon="Longitude",
            hover_name="Stadium",
            hover_data={"Team": True, "City": True, "Capacity": True},
            zoom=5,
            height=600
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(title="Stadiums in Premier League (with GPS Coordinates)")
        return fig

# Run the app
app = App(app_ui, server)
