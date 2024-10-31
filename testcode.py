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

# Define the regex pattern for filtering 2019/20 Premier League teams
pattern = r'\b(?:Liverpool|Manchester City|Manchester United|Chelsea|Leicester City|Tottenham Hotspur|Wolverhampton Wanderers|Arsenal|Sheffield United|Burnley|Southampton|Everton|Newcastle United|Crystal Palace|Brighton and Hove Albion|West Ham United|Aston Villa|Bournemouth|Watford|Norwich City)\b'

# Filter the stadiums DataFrame for only 2019/20 Premier League teams
stadiums_df = stadiums_df[stadiums_df['Team'].str.contains(pattern, case=False)]

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

# Calculate the score table
def calculate_score_table(games_df):
    # Initialize a dictionary to store team data
    teams_data = {}

    # Process each game to update team stats
    for _, row in games_df.iterrows():
        home_team, away_team = row['HomeTeam'], row['AwayTeam']
        home_goals, away_goals = row['FTHG'], row['FTAG']
        result = row['FTR']  # Result: H (Home Win), A (Away Win), D (Draw)

        if home_team not in teams_data:
            teams_data[home_team] = {"Played": 0, "Wins": 0, "Draws": 0, "Losses": 0, "GF": 0, "GA": 0, "GD": 0, "Points": 0}
        if away_team not in teams_data:
            teams_data[away_team] = {"Played": 0, "Wins": 0, "Draws": 0, "Losses": 0, "GF": 0, "GA": 0, "GD": 0, "Points": 0}

        # Update matches played and goals for each team
        teams_data[home_team]["Played"] += 1
        teams_data[away_team]["Played"] += 1
        teams_data[home_team]["GF"] += home_goals
        teams_data[home_team]["GA"] += away_goals
        teams_data[away_team]["GF"] += away_goals
        teams_data[away_team]["GA"] += home_goals

        # Update win, draw, loss, and points based on the match result
        if result == "H":
            teams_data[home_team]["Wins"] += 1
            teams_data[away_team]["Losses"] += 1
            teams_data[home_team]["Points"] += 3
        elif result == "A":
            teams_data[away_team]["Wins"] += 1
            teams_data[home_team]["Losses"] += 1
            teams_data[away_team]["Points"] += 3
        else:
            teams_data[home_team]["Draws"] += 1
            teams_data[away_team]["Draws"] += 1
            teams_data[home_team]["Points"] += 1
            teams_data[away_team]["Points"] += 1

        # Calculate goal difference
        teams_data[home_team]["GD"] = teams_data[home_team]["GF"] - teams_data[home_team]["GA"]
        teams_data[away_team]["GD"] = teams_data[away_team]["GF"] - teams_data[away_team]["GA"]

    # Convert teams_data to a DataFrame and sort by Points and GD
    score_table_df = pd.DataFrame.from_dict(teams_data, orient="index")
    score_table_df = score_table_df.sort_values(by=["Points", "GD", "GF"], ascending=[False, False, False]).reset_index()
    score_table_df.rename(columns={"index": "Team"}, inplace=True)
    return score_table_df

# Calculate the score table once
score_table_df = calculate_score_table(games_df)

# UI setup with title text
app_ui = ui.page_fluid(
    # Title and navigation bar styling
    ui.tags.head(
        ui.tags.style("""
            h1 { text-align: center; margin-top: 20px; }
            h3 { text-align: center; color: gray; margin-bottom: 20px; }
            .nav-tabs { display: flex; justify-content: center; }
            .nav-tabs .nav-item { margin: 0 10px; }
            #score_table { 
                text-align: center;
                width: 80%;
                margin: 20px auto;
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #f8f9fa;
                padding: 20px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            }
            table { 
                width: 100%; 
                border-collapse: collapse; 
                margin: 0 auto;
            }
            th, td { 
                padding: 8px 12px; 
                text-align: center; 
            }
            th { 
                background-color: #343a40; 
                color: white; 
                font-weight: bold; 
            }
            tr:nth-child(even) { 
                background-color: #f2f2f2; 
            }
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
            ui.tags.div({"id": "score_table"}, ui.output_text_verbatim("score_table"))
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
            hover_data={"Team": True, "City": True, "Capacity": True, "LogoURL": True},
            zoom=5,
            height=600
        )
        
        # Configure markers
        fig.update_traces(
            marker=dict(size=15, color="blue", symbol="circle")
        )

        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(title="Stadiums in Premier League (with GPS Coordinates)")
        
        return fig

    # Display score table in Stöðutafla tab
    @output
    @render.text
    def score_table():
        return score_table_df.to_string(index=False)

# Run the app
app = App(app_ui, server)
