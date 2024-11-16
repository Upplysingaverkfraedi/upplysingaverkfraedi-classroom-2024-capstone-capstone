import shiny
from shiny import App, render, ui
from pathlib import Path
from shiny.types import ImgData
import pandas as pd
import numpy as np
import sqlite3
from shinywidgets import output_widget, render_widget
import plotly.express as px
import plotly.graph_objects as go

# Database path
DB_PATH = '/Users/haatlason/Documents/GitHub/sqlite-greyjoy/capstone-ironislands/f1db.db'

# Set your Mapbox access token
mapbox_access_token = "pk.eyJ1IjoiYnJ5bmphcjgiLCJhIjoiY20zZzRxcGdtMDB0NDJtczZ1NWQwcGdqcyJ9.R0R4d1jbGxe9ZC0ydvT7gQ"  # Replace with your actual token
px.set_mapbox_access_token(mapbox_access_token)

# Helper Functions
def snake_to_title(snake_str):
    components = snake_str.split('_')
    return ' '.join(x.capitalize() for x in components)

def clean_column_data(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(r"[-.,]", "", regex=True)
    return df

# Mapping of race names to race IDs
race_mapping = {
    "Bahrain": 1036,
    "Emilia-Romagna": 1037,
    "Portugal": 1038,
    "Spain": 1039,
    "Monaco": 1040,
    "Azerbaijan": 1041,
    "France": 1042,
    "Styria": 1043,
    "Austria": 1044,
    "Great Britain": 1045,
    "Hungary": 1046,
    "Belgium": 1047,
    "Netherlands": 1048,
    "Italy": 1049,
    "Russia": 1050,
    "Turkey": 1051,
    "United States": 1052,
    "Mexico": 1053,
    "Brazil": 1054,
    "Qatar": 1055,
    "Saudi Arabia": 1056,
    "Abu Dhabi": 1057
}

# Load 2021 season data
def load_2021_season_data():
    # Placeholder for actual 2021 season data
    # For demonstration, using sample data
    data = pd.DataFrame({
        'Driver': ['Lewis Hamilton', 'Max Verstappen'],
        'Wins': [8, 10],
        'Podiums': [17, 18],
        'Poles': [5, 10],
        'Points': [387.5, 395.5]
    })
    return data

def get_race_comparison_data(race_id, race_name):
    query = f"""
    SELECT 
        race_id,
        type,
        position_display_order,
        position_number,
        driver_number,
        driver_id,
        constructor_id,
        engine_manufacturer_id,
        tyre_manufacturer_id,
        race_laps,
        race_time,
        race_gap,
        race_interval,
        race_points,
        race_qualification_position_number,
        race_grid_position_number,
        race_positions_gained,
        race_pit_stops,
        race_fastest_lap,
        race_driver_of_the_day,
        race_grand_slam
    FROM 
        hamilton_verstappen_race_data_2021
    WHERE 
        race_id = {race_id}
        AND type = 'RACE_RESULT'
        AND (driver_id = 'lewis-hamilton' OR driver_id = 'max-verstappen');
    """

    # Connect to the database and fetch data
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        return None

    # Rename 'position_display_order' to 'position_display_order'
    df.rename(columns={'position_display_order': 'position_display_order'}, inplace=True)

    # Define columns that need cleaning
    columns_to_clean = [
        'position_display_order',
        'race_time',
        'race_gap',
        'race_interval',
        'race_positions_gained',
        'race_pit_stops',
        'race_fastest_lap',
        'race_driver_of_the_day',
        'race_grand_slam'
    ]

    # Clean the specified columns
    df = clean_column_data(df, columns_to_clean)

    # Convert all column names from snake_case to Title Case with spaces
    df.rename(columns=lambda x: snake_to_title(x), inplace=True)

    # Prepare the data for head-to-head table
    hamilton_stats = df[df['Driver Id'] == 'lewis-hamilton'].iloc[0]
    verstappen_stats = df[df['Driver Id'] == 'max-verstappen'].iloc[0]

    # Exclude 'Race Id' and 'Driver Id' columns
    stats_columns = df.columns.drop(['Race Id', 'Driver Id']).tolist()

    # Convert numeric values to strings to avoid rendering issues
    hamilton_values = [str(hamilton_stats[col]) for col in stats_columns]
    verstappen_values = [str(verstappen_stats[col]) for col in stats_columns]

    # Construct a comparison table DataFrame
    comparison_data = {
        "Stat": stats_columns,
        "Lewis Hamilton": hamilton_values,
        "Max Verstappen": verstappen_values
    }
    comparison_df = pd.DataFrame(comparison_data)

    return comparison_df

# All-time comparison functions and data processing
def get_driver_stats(driver_id):
    conn = sqlite3.connect(DB_PATH)
    query = f"""
    SELECT 
        SUM(race_points) AS total_points,
        COUNT(CASE WHEN race_fastest_lap > 0 THEN 1 END) AS fastest_laps,
        SUM(race_positions_gained) AS positions_gained,
        SUM(race_driver_of_the_day) AS driver_of_the_day_awards,
        SUM(race_grand_slam) AS grand_slams
    FROM hamilton_verstappen_all_time_data
    WHERE driver_id = '{driver_id}'
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.iloc[0]

def scale_to_log(data):
    data = np.log(data + 1)  # Adding 1 to avoid log(0)
    return data

# Get stats for Hamilton and Verstappen
hamilton_original = get_driver_stats("lewis-hamilton")
verstappen_original = get_driver_stats("max-verstappen")

# Scale data for the plot
hamilton_values_scaled = scale_to_log(hamilton_original.values)
verstappen_values_scaled = scale_to_log(verstappen_original.values)

categories = ['Total Points', 'Fastest Laps', 'Positions Gained', 'Driver of the Day Awards', 'Grand Slams']
categoriesSpider = ['Total Points', 'Fastest Laps', 'Positions Gained', 'Driver of the Day Awards', 'Grand Slams']

# Find indices for the categories in categoriesSpider
indices = [categories.index(cat) for cat in categoriesSpider]

# Sum the scaled values for each driver
hamilton_logSpider_sum = np.sum(hamilton_values_scaled[indices])
verstappen_logSpider_sum = np.sum(verstappen_values_scaled[indices])

# Create the spider chart with scaled values and original hover text
def create_spider_chart():
    categories = categoriesSpider

    fig = go.Figure()

    # Data for Hamilton with custom hover text showing unscaled values
    fig.add_trace(go.Scatterpolar(
        r=hamilton_values_scaled,
        theta=categories,
        fill='toself',
        name='Lewis Hamilton',
        hoverinfo='text',
        hovertext=[f'{cat}: {val}' for cat, val in zip(categories, hamilton_original)]
    ))

    # Data for Verstappen with custom hover text showing unscaled values
    fig.add_trace(go.Scatterpolar(
        r=verstappen_values_scaled,
        theta=categories,
        fill='toself',
        name='Max Verstappen',
        hoverinfo='text',
        hovertext=[f'{cat}: {val}' for cat, val in zip(categories, verstappen_original)]
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(np.max(hamilton_values_scaled), np.max(verstappen_values_scaled)) + 1])
        ),
        showlegend=True
    )

    return fig

def get_points_progression(driver_id):
    conn = sqlite3.connect(DB_PATH)
    query = f"""
    SELECT race_id, race_points
    FROM hamilton_verstappen_all_time_data
    WHERE driver_id = '{driver_id}'
    ORDER BY race_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    # Calculate cumulative points
    df['cumulative_points'] = df['race_points'].cumsum()
    df['career_race'] = range(1, len(df) + 1)
    # Count wins (assuming 25 or more points indicates a win)
    wins = df[df['race_points'] >= 25].shape[0]
    return df, wins

# Get points progression for Hamilton and Verstappen
hamilton_points_progression, hamilton_wins = get_points_progression("lewis-hamilton")
verstappen_points_progression, verstappen_wins = get_points_progression("max-verstappen")

def create_points_progression_chart(x_axis='career_race'):
    fig = go.Figure()

    # Data for Hamilton
    fig.add_trace(go.Scatter(
        x=hamilton_points_progression[x_axis],
        y=hamilton_points_progression['cumulative_points'],
        mode='lines+markers',
        line=dict(shape='spline', smoothing=1.3, width=3),
        name='Lewis Hamilton',
        hoverinfo='text',
        hovertext=[f"Race {race}: {points} pts, Cumulative: {cumulative} pts"
                   for race, points, cumulative in zip(
                hamilton_points_progression['career_race'],
                hamilton_points_progression['race_points'],
                hamilton_points_progression['cumulative_points'])]
    ))

    # Mark winning races for Hamilton
    hamilton_winning_races = hamilton_points_progression[hamilton_points_progression['race_points'] >= 25]
    fig.add_trace(go.Scatter(
        x=hamilton_winning_races[x_axis],
        y=hamilton_winning_races['cumulative_points'],
        mode='markers',
        marker=dict(color='gold', size=10, symbol='star'),
        name='Hamilton Winning Races',
        hoverinfo='text',
        hovertext=[f"Race {race}: {points} pts, Cumulative: {cumulative} pts"
                   for race, points, cumulative in zip(
                hamilton_winning_races['career_race'],
                hamilton_winning_races['race_points'],
                hamilton_winning_races['cumulative_points'])]
    ))

    # Data for Verstappen
    fig.add_trace(go.Scatter(
        x=verstappen_points_progression[x_axis],
        y=verstappen_points_progression['cumulative_points'],
        mode='lines+markers',
        line=dict(shape='spline', smoothing=1.3, width=3),
        name='Max Verstappen',
        hoverinfo='text',
        hovertext=[f"Race {race}: {points} pts, Cumulative: {cumulative} pts"
                   for race, points, cumulative in zip(
                verstappen_points_progression['career_race'],
                verstappen_points_progression['race_points'],
                verstappen_points_progression['cumulative_points'])]
    ))

    # Mark winning races for Verstappen
    verstappen_winning_races = verstappen_points_progression[verstappen_points_progression['race_points'] >= 25]
    fig.add_trace(go.Scatter(
        x=verstappen_winning_races[x_axis],
        y=verstappen_winning_races['cumulative_points'],
        mode='markers',
        marker=dict(color='gold', size=10, symbol='star'),
        name='Verstappen Winning Races',
        hoverinfo='text',
        hovertext=[f"Race {race}: {points} pts, Cumulative: {cumulative} pts"
                   for race, points, cumulative in zip(
                verstappen_winning_races['career_race'],
                verstappen_winning_races['race_points'],
                verstappen_winning_races['cumulative_points'])]
    ))

    fig.update_layout(
        title="Points Progression Over Time with Winning Races Highlighted",
        xaxis_title="Career Race Number" if x_axis == 'career_race' else "Race ID",
        yaxis_title="Cumulative Points",
        legend_title="Driver",
        showlegend=True
    )

    return fig

def get_fastest_lap_data():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT race_id, driver_id, fastest_lap_time_millis
    FROM hamilton_verstappen_all_time_data
    WHERE fastest_lap_time_millis IS NOT NULL
    ORDER BY race_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def prepare_heatmap_data(df):
    # Use pivot_table with mean aggregation to handle duplicates
    heatmap_data = df.pivot_table(
        index="driver_id",
        columns="race_id",
        values="fastest_lap_time_millis",
        aggfunc='mean'
    )
    heatmap_data = heatmap_data.fillna(0)
    return heatmap_data

def create_fastest_lap_heatmap():
    # Prepare data
    fastest_lap_data = get_fastest_lap_data()
    heatmap_data = prepare_heatmap_data(fastest_lap_data)
    drivers = heatmap_data.index.tolist()
    races = heatmap_data.columns.tolist()
    z_values = heatmap_data.values

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=races,
        y=drivers,
        colorscale='Viridis',
        colorbar=dict(title="Fastest Lap Time (ms)")
    ))

    fig.update_layout(
        title=dict(text="Fastest Lap Times per Race"),
        xaxis=dict(title="Race ID"),
        yaxis=dict(title="Driver")
    )

    return fig

def get_location_and_performance_data():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT 
        l.race_id,
        l.grand_prix_id, 
        l.circuit_id, 
        l.lat, 
        l.lon, 
        p.driver_id, 
        p.race_points 
    FROM race_locations AS l
    JOIN hamilton_verstappen_all_time_data AS p ON l.race_id = p.race_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    # Fill NaN values in race_points with 0
    df['race_points'] = df['race_points'].fillna(0)
    return df

# Get location and performance data
location_performance_data = get_location_and_performance_data()

def get_average_points(data):
    avg_data = data.groupby(['circuit_id', 'lat', 'lon', 'driver_id']).race_points.mean().reset_index()
    avg_data.rename(columns={'race_points': 'avg_points'}, inplace=True)
    return avg_data

def create_performance_map(data):
    # Use average points
    data = get_average_points(data)

    # Ensure data has no missing values in required columns
    data = data.dropna(subset=['lat', 'lon', 'avg_points'])

    fig = px.scatter_mapbox(
        data,
        lat="lat",
        lon="lon",
        color="driver_id",
        size="avg_points",
        hover_name="circuit_id",
        hover_data={
            "driver_id": True,
            "avg_points": True,
            "lat": False,
            "lon": False
        },
        title="Average Performance by Location for Hamilton and Verstappen",
        labels={"driver_id": "Driver", "avg_points": "Average Points"},
        mapbox_style="light",
        zoom=1,
        height=600
    )

    # Update layout with the access token correctly
    fig.update_layout(mapbox_accesstoken=mapbox_access_token)
    return fig

# Define UI
app_ui = ui.page_fluid(
    # Header with F1 logo, images, and title, with a red background and white title text
    ui.div(
        ui.row(
            # Hamilton Image on the left
            ui.column(
                3,
                ui.div(
                    ui.output_image("hamilton_image"),
                    style="text-align:center; margin: 0; padding: 0; height: 200px"
                )
            ),
            # F1 Logo in the center
            ui.column(
                6,
                ui.div(
                    ui.output_image("f1logo_image"),
                    style="text-align:center; margin: 0; padding: 0; height: 120px"
                )
            ),
            # Verstappen Image on the right
            ui.column(
                3,
                ui.div(
                    ui.output_image("verstappen_image"),
                    style="text-align:center; margin: 0; padding: 0; height: 200px"
                )
            ),
            # Row style to center images and logo
            style="display: flex; align-items: center; justify-content: center; margin-bottom: 0;"
        ),
        # Title centered below the images and logo
        ui.div(
            ui.h2(
                "Lewis Hamilton VS Max Verstappen",
                style="margin: -15px; padding: 0; font-size: 28px; color: white; font-family: Monaco, monospace; text-align: center;"
            ),
            style="margin-top: 0;"
        ),
        # Apply the red background color and set fixed height for header
        style="background-color: red; color: white; height: 220px;"
    ),
    # Tabs for organizing content using ui.navset_tab and ui.nav_panel
    ui.navset_tab(
        ui.nav_panel(
            "All-time Comparison",
            ui.h2("Lewis Hamilton VS Max Verstappen Overview"),
            ui.page_fillable(
                ui.layout_columns(
                    ui.card(ui.h3("Log-scaled Spider Chart"),
                            ui.layout_columns(
                                ui.card(
                                    ui.h4("Spider Chart"),
                                    output_widget("spider_chart")
                                ),
                                ui.layout_column_wrap(
                                    ui.card(
                                        ui.h5("Lewis Hamilton log-scaled sum"),
                                        ui.p("{hamilton_logSpider_sum:.2f}")
                                    ),
                                    ui.card(
                                        ui.h5("Max Verstappen log-scaled sum"),
                                        ui.p("{verstappen_logSpider_sum:.2f}")
                                    ),
                                    col_width=6
                                ),
                                col_widths=[12, 4],
                            )
                            ),
                    ui.card(ui.h3("Points over Time"),
                            ui.layout_columns(
                                ui.card(
                                    output_widget("points_progression_chart")
                                ),
                                ui.card(
                                    ui.input_radio_buttons(
                                        "x_axis_radio",
                                        ui.h4("Choose X-axis"),
                                        choices={"career_race": "Career Race", "race_id": "Race ID"},
                                        selected="career_race"),
                                ),
                                ui.layout_column_wrap(
                                    ui.card(
                                        ui.h5("Lewis Hamilton wins"),
                                        ui.p("{hamilton_wins:.0f}")
                                    ),
                                    ui.card(
                                        ui.h5("Max Verstappen wins"),
                                        ui.p("{verstappen_wins:.0f}")
                                    ),
                                ),
                                col_widths=[12, 4, 4]
                            )
                            ),
                    ui.card(ui.h3("Heatmap of Fastest Laps"),
                            output_widget("fastest_lap_heatmap")
                            ),
                    ui.card(ui.h3("Map of Performance by Location"),
                            output_widget("performance_map")
                            ),
                    col_widths=[12, 12, 12],
                )
            )
        ),
        ui.nav_panel(
            "2021 Season Comparison",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.input_select(
                        "race_select",
                        "Select a Race:",
                        choices=["2021 Season Overview"] + list(race_mapping.keys()),
                        selected="2021 Season Overview"
                    ),
                ),
                # Main content area that updates based on selected race
                ui.div(
                    ui.output_ui("race_content")
                )
            )
        )
    )
)

# Define Server Logic
def server(input, output, session):
    # Load 2021 season overview data
    data = load_2021_season_data()

    # Render the Hamilton image
    @output
    @render.image
    def hamilton_image():
        img_path = Path(__file__).parent / "www" / "hamilton.jpeg"
        if img_path.exists():
            img: ImgData = {
                "src": str(img_path),
                "width": "200px",
                "height": "200px",
                "style": "border:5px solid Turquoise;"
            }
            return img
        else:
            return {
                "src": "",
                "alt": "Lewis Hamilton image not found."
            }

    # Render the Verstappen image
    @output
    @render.image
    def verstappen_image():
        img_path = Path(__file__).parent / "www" / "verstappen.jpeg"
        if img_path.exists():
            img: ImgData = {
                "src": str(img_path),
                "width": "200px",
                "height": "200px",
                "style": "border:5px solid blue;"
            }
            return img
        else:
            return {
                "src": "",
                "alt": "Max Verstappen image not found."
            }

    # Render the F1 logo image
    @output
    @render.image
    def f1logo_image():
        img_path = Path(__file__).parent / "www" / "f1logo.png"
        if img_path.exists():
            img: ImgData = {
                "src": str(img_path),
                "width": "120px",
                "height": "120px",
                "style": "border:2px solid white;"
            }
            return img
        else:
            return {
                "src": "",
                "alt": "F1 Logo image not found."
            }

    # Outputs for "All-time Comparison" tab
    @output
    @render_widget
    def spider_chart():
        return create_spider_chart()

    @output
    @render_widget
    def points_progression_chart():
        x_axis_choice = input.x_axis_radio()
        return create_points_progression_chart(x_axis=x_axis_choice)

    @output
    @render_widget
    def fastest_lap_heatmap():
        return create_fastest_lap_heatmap()

    @output
    @render_widget
    def performance_map():
        return create_performance_map(location_performance_data)

    # Reactive output for race content in "2021 Season Comparison" tab
    @output
    @render.ui
    def race_content():
        race = input.race_select()
        if race == "2021 Season Overview":
            # Display the driver statistics table along with images and title
            return ui.TagList(
                # Integrated Title and Images
                ui.page_fluid(
                    # Centered title
                    ui.tags.div(
                        ui.h2("Keppnisbílar Lewis Hamilton og Max Verstappen"),
                        style="text-align: center; font-family: Monaco, monospace; margin-top: 20px;"
                    ),
                    # Row for the two images and their captions
                    ui.row(
                        # Column for Lewis Hamilton's car
                        ui.column(
                            6,  # Half the width
                            ui.div(
                                ui.h3("Bíll Lewis Hamilton - Mercedes Benz W12"),
                                style="text-align: center; font-family: Monaco, monospace; font-size: 12px; margin-top: 10px;"
                            ),
                            ui.output_image("hamilton_car_image")
                        ),
                        # Column for Max Verstappen's car
                        ui.column(
                            6,  # Half the width
                            ui.div(
                                ui.h3("Bíll Max Verstappen - Honda RB16B"),
                                style="text-align: center; font-family: Monaco, monospace; font-size: 12px; margin-top: 10px;"
                            ),
                            ui.output_image("verstappen_car_image")
                        )
                    ),
                    # Styling for the overall section
                    style="margin-bottom: 30px;"
                ),
                # Driver Statistics Table
                ui.h3("2021 Season Overview"),
                ui.output_table("driver_table")
            )
        else:
            # For selected races, display the head-to-head comparison table and track image
            return ui.TagList(
                ui.h3(f"Head-to-Head Comparison for {race}"),
                ui.output_image("track_image"),  # Display track image
                ui.output_table("race_comparison_table")
            )

    # Render driver statistics table
    @output
    @render.table
    def driver_table():
        # For demonstration, return the sample data
        return data

    # Render race comparison table
    @output
    @render.table
    def race_comparison_table():
        race = input.race_select()
        race_id = race_mapping.get(race)
        if race_id:
            comparison_df = get_race_comparison_data(race_id, race)
            if comparison_df is not None:
                return comparison_df
            else:
                return pd.DataFrame({"Message": [f"No data available for {race}"]})
        else:
            return pd.DataFrame({"Message": [f"Race ID not found for {race}"]})

    # Render track image based on selected race
    @output
    @render.image
    def track_image():
        race = input.race_select()
        if race == "2021 Season Overview":
            return None  # No image for the overview
        else:
            # Generate the file name based on the race name
            # Handle special characters and spaces
            image_name = race.lower().replace(" ", "_").replace("-", "_") + ".png"
            img_path = Path(__file__).parent / "www" / image_name
            if img_path.exists():
                img: ImgData = {
                    "src": str(img_path),
                    "width": "600px",  # Adjust the width as needed
                    "height": "auto",
                    "style": "display: block; margin-left: auto; margin-right: auto; margin-top: 20px;"
                }
                return img
            else:
                # Optionally, return a default image or an error message
                # Here, returning an alt text
                return {
                    "src": "",
                    "alt": f"Image for {race} not found."
                }

    # Render images for the 2021 Season Overview
    @output
    @render.image
    def hamilton_car_image():
        img_path = Path(__file__).parent / "Bilamyndir" / "LewisHamiltonBill.jpeg"
        if img_path.exists():
            img: ImgData = {
                "src": str(img_path),
                "width": "300px",
                "height": "150px",
                "style": "border:5px solid Turquoise;",
                "alt": "Bíll Lewis Hamilton árið 2021"
            }
            return img
        else:
            return {
                "src": "",
                "alt": "Lewis Hamilton car image not found."
            }

    @output
    @render.image
    def verstappen_car_image():
        img_path = Path(__file__).parent / "Bilamyndir" / "MaxVerstappenBill.jpeg"
        if img_path.exists():
            img: ImgData = {
                "src": str(img_path),
                "width": "300px",
                "height": "150px",
                "style": "border:5px solid blue;",
                "alt": "Bíll Max Verstappen árið 2021"
            }
            return img
        else:
            return {
                "src": "",
                "alt": "Max Verstappen car image not found."
            }

# Create the Shiny app
app = App(app_ui, server)
