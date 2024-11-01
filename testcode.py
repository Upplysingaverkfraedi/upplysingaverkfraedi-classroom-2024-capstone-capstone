import sqlite3
import pandas as pd
from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_plotly
import plotly.express as px

# Load CSV files into DataFrames
games_df = pd.read_csv('Games_season19-20.csv')
stadiums_df = pd.read_csv('stadiums-with-GPS-coordinates.csv')

# Define function to calculate league table for a specific game week and get last 5 games
def calculate_league_table(games_df, game_week):
    teams_data = {}
    last_5_games = {}

    # Filter games up to the selected game week
    weekly_games = games_df[games_df['GW'] <= game_week]

    for _, row in weekly_games.iterrows():
        home_team, away_team = row['HomeTeam'], row['AwayTeam']
        home_goals, away_goals = row['FTHG'], row['FTAG']
        result = row['FTR']

        # Initialize team data if not present
        if home_team not in teams_data:
            teams_data[home_team] = {"Played": 0, "W": 0, "D": 0, "L": 0, "+/-": 0, "PTS": 0}
            last_5_games[home_team] = []
        if away_team not in teams_data:
            teams_data[away_team] = {"Played": 0, "W": 0, "D": 0, "L": 0, "+/-": 0, "PTS": 0}
            last_5_games[away_team] = []

        # Update matches played and goals for each team
        teams_data[home_team]["Played"] += 1
        teams_data[away_team]["Played"] += 1
        teams_data[home_team]["+/-"] += (home_goals - away_goals)
        teams_data[away_team]["+/-"] += (away_goals - home_goals)

        # Determine result for home and away teams and add to last 5 games list
        if result == "H":
            teams_data[home_team]["W"] += 1
            teams_data[home_team]["PTS"] += 3
            teams_data[away_team]["L"] += 1
            last_5_games[home_team].insert(0, f"{home_team} vs {away_team} = W")
            last_5_games[away_team].insert(0, f"{away_team} vs {home_team} = L")
        elif result == "A":
            teams_data[away_team]["W"] += 1
            teams_data[away_team]["PTS"] += 3
            teams_data[home_team]["L"] += 1
            last_5_games[away_team].insert(0, f"{away_team} vs {home_team} = W")
            last_5_games[home_team].insert(0, f"{home_team} vs {away_team} = L")
        else:
            teams_data[home_team]["D"] += 1
            teams_data[away_team]["D"] += 1
            teams_data[home_team]["PTS"] += 1
            teams_data[away_team]["PTS"] += 1
            last_5_games[home_team].insert(0, f"{home_team} vs {away_team} = D")
            last_5_games[away_team].insert(0, f"{away_team} vs {home_team} = D")

        # Keep only the last 5 games
        last_5_games[home_team] = last_5_games[home_team][:5]
        last_5_games[away_team] = last_5_games[away_team][:5]

    # Convert teams_data to a DataFrame and sort by Points and GD
    league_table_df = pd.DataFrame.from_dict(teams_data, orient="index")
    league_table_df = league_table_df.sort_values(by=["PTS", "+/-"], ascending=[False, False]).reset_index()
    league_table_df.rename(columns={"index": "Team"}, inplace=True)
    league_table_df['POS'] = league_table_df.index + 1  # Adding position for display
    return league_table_df, last_5_games

# UI setup with title text and improved styling
app_ui = ui.page_fluid(
    ui.tags.div(
        ui.h1("Enska Úrvalsdeildin", style="text-align: center; color: #38003c;"),
        ui.h3("2019/20", style="text-align: center; color: gray;"),
    ),
    
    ui.navset_tab(
        ui.nav_panel(
            "Heim",
            ui.h2("Premier League Home"),
            ui.p("Welcome to the Premier League Analysis.")
        ),
        ui.nav_panel(
            "Stöðutafla",
            ui.h2("League Table"),
            ui.tags.div(
                {"class": "slider-container", "style": "text-align: center; margin-bottom: 20px;"},
                ui.input_slider("game_week", "Select Game Week:", min=1, max=38, value=1)
            ),
            ui.tags.div({"id": "score_table"}, ui.output_ui("score_table_ui"))
        ),
        ui.nav_panel(
            "Staðsetningar",
            ui.h2("Stadiums with GPS Coordinates"),
            output_widget("stadiums_map"),
            ui.p("Map of stadiums in the Premier League with GPS coordinates.")
        ),
    )
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

    # Display score table in Stöðutafla tab
    @reactive.Calc
    def filtered_league_table():
        return calculate_league_table(games_df, input.game_week())

    @output
    @render.ui
    def score_table_ui():
        league_table_df, last_5_games = filtered_league_table()
        
        # Build the table UI with collapsible rows for last 5 games
        rows = []
        header = "{:<4} {:<15} {:^6} {:^4} {:^4} {:^4} {:^4} {:^6}".format("POS", "Team", "PL", "W", "D", "L", "+/-", "PTS")
        rows.append(ui.tags.pre(header))
        
        for _, row in league_table_df.iterrows():
            # Row for the main team info
            main_row = "{:<4} {:<15} {:^6} {:^4} {:^4} {:^4} {:^4} {:^6}".format(
                row['POS'], row['Team'], row['Played'], row['W'], row['D'], row['L'], row['+/-'], row['PTS']
            )
            rows.append(ui.tags.details(
                ui.tags.summary(main_row),
                ui.tags.ul([ui.tags.li(match) for match in last_5_games[row['Team']]])
            ))
        
        return ui.tags.div(*rows)

# Run the app
app = App(app_ui, server)
