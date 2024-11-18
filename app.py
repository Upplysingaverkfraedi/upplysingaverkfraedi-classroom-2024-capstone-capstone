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
import datetime

# Database path
DB_PATH = 'f1db.db'
con = sqlite3.connect(DB_PATH)

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

def get_race_comparison_data(race_id, race):
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
    data = data.copy()
    data = np.log(data + 1)  # Adding 1 to avoid log(0)
    data['total_points'] = data['total_points'] / 1.9
    data['grand_slams'] = data['grand_slams'] * 2
    data['driver_of_the_day_awards'] = data['driver_of_the_day_awards'] * 1.2
    data['fastest_laps'] = data['fastest_laps'] * 1.1
    data['grand_slams'] = data['grand_slams'] * 1.2
    data['positions_gained'] = data['positions_gained'] * 0.9
    return data

# Get stats for Hamilton and Verstappen
hamilton_original = get_driver_stats("lewis-hamilton")
verstappen_original = get_driver_stats("max-verstappen")

# Scale data for the plot
hamilton_values_scaled = scale_to_log(hamilton_original)
verstappen_values_scaled = scale_to_log(verstappen_original)

categories = ['Total Points', 'Fastest Laps', 'Positions Gained', 'Driver of the Day Awards', 'Grand Slams']
categoriesSpider = ['Total Points', 'Fastest Laps', 'Positions Gained', 'Driver of the Day Awards', 'Grand Slams']

# Find indices for the categories in categoriesSpider
indices = [categories.index(cat) for cat in categoriesSpider]

# Sum the scaled values for each driver
#hamilton_logSpider_sum = np.sum(hamilton_values_scaled[indices])
#verstappen_logSpider_sum = np.sum(verstappen_values_scaled[indices])

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
            bgcolor="#f9f9f9",  # Ljós bakgrunnur í polar plot
            angularaxis=dict(
                tickfont=dict(size=14, color="black"),  # Stærri og dekkri texti fyrir flokka
                linewidth=2,  # Dekkri línur fyrir flokka
                linecolor="black",  # Svartar línur frá miðju í flokka
                ticks='outside',  # Ticks utan á ásnum
                ticklen=5  # Lengd ticks
            ),
            radialaxis=dict(
                showticklabels=False,  # Fjarlægir tölur á radial ásnum
                gridcolor="lightgray",  # Minna áberandi netlínur
                gridwidth=0.8,  # Þynnri netlínur
                linecolor="gray",  # Minna áberandi radial ás
                linewidth=0.8  # Þynnri radial línur
            )
        ),
        showlegend=True,
        legend=dict(
            font=dict(size=12),
            orientation="h",
            yanchor="bottom",
            y=1.1,
            xanchor="center",
            x=0.5
        ),
        template="plotly_white"
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

    # Gögn fyrir Hamilton
    fig.add_trace(go.Scatter(
        x=hamilton_points_progression[x_axis],
        y=hamilton_points_progression['cumulative_points'],
        mode='lines+markers',
        line=dict(shape='spline', smoothing=1.3, width=3, color='blue'),
        name='Lewis Hamilton',
        hoverinfo='text',
        hovertext=[f"Race {race}: {points} pts, Cumulative: {cumulative} pts"
                   for race, points, cumulative in zip(
                hamilton_points_progression[x_axis],
                hamilton_points_progression['race_points'],
                hamilton_points_progression['cumulative_points'])]
    ))

    # Merkja sigurkeppnir Hamilton
    hamilton_winning_races = hamilton_points_progression[hamilton_points_progression['race_points'] >= 25]
    fig.add_trace(go.Scatter(
        x=hamilton_winning_races[x_axis],
        y=hamilton_winning_races['cumulative_points'],
        mode='markers',
        marker=dict(color='gold', size=5, symbol='star'),
        name='Hamilton Wins',
        hoverinfo='text',
        hovertext=[f"Race {race}: {points} pts, Cumulative: {cumulative} pts"
                   for race, points, cumulative in zip(
                hamilton_winning_races[x_axis],
                hamilton_winning_races['race_points'],
                hamilton_winning_races['cumulative_points'])]
    ))

    # Gögn fyrir Verstappen
    fig.add_trace(go.Scatter(
        x=verstappen_points_progression[x_axis],
        y=verstappen_points_progression['cumulative_points'],
        mode='lines+markers',
        line=dict(shape='spline', smoothing=1.3, width=3, color='red'),
        name='Max Verstappen',
        hoverinfo='text',
        hovertext=[f"Race {race}: {points} pts, Cumulative: {cumulative} pts"
                   for race, points, cumulative in zip(
                verstappen_points_progression[x_axis],
                verstappen_points_progression['race_points'],
                verstappen_points_progression['cumulative_points'])]
    ))

    # Merkja sigurkeppnir Verstappen
    verstappen_winning_races = verstappen_points_progression[verstappen_points_progression['race_points'] >= 25]
    fig.add_trace(go.Scatter(
        x=verstappen_winning_races[x_axis],
        y=verstappen_winning_races['cumulative_points'],
        mode='markers',
        marker=dict(color='silver', size=5, symbol='star'),
        name='Verstappen Wins',
        hoverinfo='text',
        hovertext=[f"Race {race}: {points} pts, Cumulative: {cumulative} pts"
                   for race, points, cumulative in zip(
                verstappen_winning_races[x_axis],
                verstappen_winning_races['race_points'],
                verstappen_winning_races['cumulative_points'])]
    ))

    # Uppfærsla á útliti
    fig.update_layout(
        title="Points Progression Over Time with Winning Races Highlighted",
        xaxis=dict(
            title="Career Race Number" if x_axis == 'career_race' else "Race ID",
            showgrid=True
        ),
        yaxis=dict(
            title="Cumulative Points",
            showgrid=True
        ),
        legend_title="Driver",
        template="plotly_white",
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
        colorscale='Plasma',
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

def get_location_and_performance_data_2021():
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
    JOIN hamilton_verstappen_race_data_2021 AS p ON l.race_id = p.race_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    # Fill NaN values in race_points with 0
    df['race_points'] = df['race_points'].fillna(0)
    return df

location_performance_data_2021 = get_location_and_performance_data_2021()

def get_average_points(data):
    avg_data = data.groupby(['circuit_id', 'lat', 'lon', 'driver_id']).race_points.mean().reset_index()
    avg_data.rename(columns={'race_points': 'avg_points'}, inplace=True)
    return avg_data

def create_performance_map(data):
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

def create_performance_map_with_race_points(data):
    # Fjarlægja línur með vantar breytur í nauðsynlegum dálkum
    data = data.dropna(subset=['lat', 'lon', 'race_points'])

    fig = px.scatter_mapbox(
        data,
        lat="lat",
        lon="lon",
        color="driver_id",
        size="race_points",
        hover_name="circuit_id",
        hover_data={
            "driver_id": True,
            "race_points": True,
            "lat": False,
            "lon": False
        },
        title="Race Points by Location for Hamilton and Verstappen",
        labels={"driver_id": "Driver", "race_points": "Race Points"},
        mapbox_style="light",
        zoom=1,
        height=600
    )

    # Update layout with access token and map style
    fig.update_layout(mapbox_accesstoken=mapbox_access_token)
    return fig


# Búa til valmöguleika fyrir framleiðanda flokka
manufacturer_choices = {
    "Vélaframleiðandi": "engine_manufacturer_id",
    "Dekkjaframleiðandi": "tyre_manufacturer_id",
    "Lið": "constructor_id"
}

# Fetch laps and distance data from the database
def get_race_details(race_name):
    race_id = race_mapping.get(race_name)
    if not race_id:
        return None
    
    query = f"""
    SELECT laps, distance
    FROM race
    WHERE id = {race_id}
    """
    conn = sqlite3.connect(DB_PATH)
    result = pd.read_sql_query(query, conn)
    conn.close()
    
    if result.empty:
        return None
    
    return result.iloc[0].to_dict()

def get_race_points(race_name):
    
    race_id = race_mapping.get(race_name)
    query = f"""
    SELECT driver_id, race_points
    FROM hamilton_verstappen_race_data_2021
    WHERE race_id = {race_id} AND type = 'RACE_RESULT'
    """
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def convert_time_to_seconds(time_str):
    if time_str is None:  # Athuga hvort gildið sé None
        return None
    try:
        # Breytir tímanum í datetime object og svo í sekúndur
        t = datetime.datetime.strptime(time_str, "%H:%M:%S.%f")
        return t.hour * 3600 + t.minute * 60 + t.second + t.microsecond / 1e6
    except ValueError:
        # Ef tíminn er ekki á réttu formi, skilaðu None
        return None
    
def convert_lap_time_to_seconds(lap_time_str):
    try:
        # Skipta strengnum í mínútur og sekúndur.millisekúndur
        minutes, seconds = lap_time_str.split(":")
        return int(minutes) * 60 + float(seconds)  # Umbreyta í sekúndur
    except (ValueError, TypeError):
        return None  # Skila None ef umbreyting mistekst
    
def convert_time_to_seconds_2(time_str):
    try:
        # Ef tíminn er á sniði mínútur:sekúndur.millisekúndur (t.d., "1:11.497")
        if ":" in time_str:
            minutes, seconds = time_str.split(":")
            return int(minutes) * 60 + float(seconds)
        # Ef tíminn er á sniði sekúndur.millisekúndur (t.d., "59.926")
        else:
            return float(time_str)
    except (ValueError, TypeError):
        return None  # Skila None ef umbreyting mistekst





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
            ui.layout_sidebar(
                # Sidebar fyrir valkosti
                ui.sidebar(
                    ui.input_radio_buttons(
                        "x_axis_radio",
                        ui.h4("Choose X-axis"),
                        choices={"career_race": "Career Race", "race_id": "Race ID"},
                        selected="career_race"
                    )
                ),
                ui.page_fillable(
                    ui.layout_columns(
                        ui.card(
                            output_widget("wins_bar_chart")  # Hér birtist nýja súluritið
                        ),
                        ui.card(
                            output_widget("points_progression_chart")
                        ),
                        ui.card(
                            output_widget("performance_map_1")
                        ),
                        ui.card("Samanburður á Lewis Hamilton og Max Verstappen",
                                output_widget("spider_chart")
                        ),
                        ui.card(
                            output_widget("fastest_lap_heatmap")
                        ),
                    col_widths=[4,8,8,4,12],
                    )
                )
            ),
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
        ),
        ui.nav_panel(
            "Framleiðenda Frammistaða",
            ui.input_select("manufacturer_type", "Veldu Flokk", choices=list(manufacturer_choices.keys())),
            output_widget("manufacturer_average_points_plot"),
            output_widget("manufacturer_total_points_plot")
        )
    )
)

# Define Server Logic
def server(input, output, session):
    # Load 2021 season overview data
    data = load_2021_season_data()
    
    # Snúa töflunni
    transposed_data = data.set_index("Driver").transpose()

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
    def performance_map_1():
        return create_performance_map(location_performance_data)
    
    @output
    @render_widget
    def performance_map_3():
        return create_performance_map(location_performance_data_2021)
    
    
    @output
    @render_widget
    def performance_map_2():
        race = input.race_select()
        
        # Athugaðu hvort valið keppni er til í race_mapping
        if race in race_mapping:
            race_id = race_mapping[race]
            
            # Sía gögnin fyrir valda keppnina
            filtered_data = location_performance_data_2021[location_performance_data_2021['race_id'] == race_id]
            
            # Athugaðu hvort síuð gögn eru til
            if not filtered_data.empty:
                return create_performance_map_with_race_points(filtered_data)
            else:
                # Skila tómu korti eða skilaboðum ef engin gögn eru til
                fig = px.scatter_mapbox(
                    [],
                    lat=[],
                    lon=[],
                    mapbox_style="light",
                    title=f"Engar upplýsingar fyrir {race}",
                    height=600
                )
                return fig
        else:
            # Skila tómu korti eða skilaboðum ef valið keppni finnst ekki
            fig = px.scatter_mapbox(
                [],
                lat=[],
                lon=[],
                mapbox_style="light",
                title="Valin keppni er ekki gild.",
                height=600
            )
            return fig


    # Reactive output for race content in "2021 Season Comparison" tab
    @output
    @render.ui
    def race_content():
        race = input.race_select()
        if race == "2021 Season Overview":
            # Display the driver statistics table along with images and title
            return ui.TagList(
                # Integrated Title and 3D Models
                ui.page_fluid(
                    # Centered title
                    ui.tags.div(
                        ui.h2("Keppnisbílar Lewis Hamilton og Max Verstappen"),
                        style="text-align: center; font-family: Monaco, monospace; margin-top: 20px;"
                    ),
                    # Row for the two 3D models and their captions
                    ui.row(
                        # Column for Lewis Hamilton's car
                        ui.column(
                            6,  # Half the width
                            ui.div(
                                ui.h3("Bíll Lewis Hamilton - Mercedes Benz W12"),
                                style="text-align: center; font-family: Monaco, monospace; font-size: 12px; margin-top: 10px;"
                            ),
                            ui.tags.div(
                                ui.tags.iframe(
                                    title="Mercedes AMG F1 W12 E Performance 2021",
                                    src="https://sketchfab.com/models/e586353e96384dd6a306db3dd56ae7ea/embed",
                                    frameborder="0",
                                    allow="autoplay; fullscreen; xr-spatial-tracking",
                                    mozallowfullscreen="true",
                                    webkitallowfullscreen="true",
                                    width="100%",
                                    height="400px"
                                ),
                                style="text-align: center;"
                            )
                        ),
                        # Column for Max Verstappen's car
                        ui.column(
                            6,  # Half the width
                            ui.div(
                                ui.h3("Bíll Max Verstappen - Honda RB16B"),
                                style="text-align: center; font-family: Monaco, monospace; font-size: 12px; margin-top: 10px;"
                            ),
                            ui.tags.div(
                                ui.tags.iframe(
                                    title="Red Bull Racing F1 Car - RB16B 2021 Season",
                                    src="https://sketchfab.com/models/3c76346ee84242099675f4de8cbbd587/embed",
                                    frameborder="0",
                                    allow="autoplay; fullscreen; xr-spatial-tracking",
                                    mozallowfullscreen="true",
                                    webkitallowfullscreen="true",
                                    width="100%",
                                    height="400px"
                                ),
                                style="text-align: center;"
                            )
                        )
                    ),
                    # Styling for the overall section
                    style="margin-bottom: 30px;"
                ),
                # Driver Statistics Table
                ui.h3("2021 Season Overview"),
                ui.layout_columns(
                ui.card(output_widget("vertical_points_chart")), # Sýna upprunalegu gögnin
                ui.card(output_widget("hamilton_verstappen_cumulative_plot")),
                ui.card(output_widget("hamilton_verstappen_position_plot")),
                ui.card(output_widget("horizontal_bar_chart")), # Sýna lárétt súlurit
                ui.card(output_widget("performance_map_3")), # Sýna töflu # Sýna töflu
                col_widths=[4, 8, 6, 6, 12]
                )
            )
        else:
            race_details = get_race_details(race)
            if not race_details:
                race_details_text = "No details available for this race."
            else:
                race_details_text = f"""
                Laps: {race_details['laps']}<br>
                Distance: {race_details['distance']} km
                """

            return ui.TagList(
                ui.h3(f"Head-to-Head Comparison for {race}"),
                ui.layout_columns(
                    ui.card( 
                        ui.layout_columns( ui.card(
                            ui.output_image("track_image")),
                            ui.card(
                                ui.div(
                                    ui.h4("Race Details"),
                                    ui.HTML(race_details_text),
                                    style="text-align: left; padding: 10px;"
                                )
                            ),
                            col_widths=[12, 6]
                        )
                    ),
                    ui.card(
                        ui.h4("Head-to-Head Comparison"),
                        output_widget("performance_map_2")
                    ),
                    ui.card(output_widget("horizontal_pit_stop_comparison_chart")),
                    ui.card(output_widget("vertical_comparison_barplot")),
                    ui.card(output_widget("horizontal_race_time_comparison_chart")),
                     ui.card(output_widget("start_vs_finish_positions_chart")),
                    ui.card(output_widget("fastest_lap_chart")), 
                    ui.card(output_widget("positions_gained_bar_chart")),
                    col_widths=[8, 4, 4, 8, 6, 6,6,6]
                ),
            )
            
    # Render driver statistics table
    @output
    @render.table
    def driver_table():
        # For demonstration, return the sample data
        return transposed_data
    
    # Sýna lárétt súlurit
    @output
    @render_widget
    def horizontal_bar_chart():
        # Snúa gögnunum án 'Points'
        melted_data = data.drop(columns=["Points"]).melt(
            id_vars=["Driver"], var_name="Metric", value_name="Value"
        )

        # Plotly súlurit
        fig = go.Figure()

        # Bæta við súlum fyrir hvern ökumann
        for driver in data["Driver"]:
            driver_data = melted_data[melted_data["Driver"] == driver]
            fig.add_trace(go.Bar(
                y=driver_data["Metric"],  # Láréttar breytur
                x=driver_data["Value"],  # Gildin fyrir hverja breytu
                name=driver,
                orientation='h'  # Lárétt súlurit
            ))

        # Uppsetning lárétta súluritsins
        fig.update_layout(
            title="2021 Performance (Wins, Podiums, Poles)",
            xaxis_title="Value",
            yaxis_title="Metric",
            barmode="group",
            height=400,
            legend_title="Driver",
            template="plotly_white"
        )

        return fig
    
    @output
    @render_widget
    def vertical_points_chart():
        # Plotly lóðrétt súlurit fyrir Points
        fig = go.Figure()

        # Bæta við súlum fyrir hvern ökumann
        for driver in data["Driver"]:
            driver_data = data[data["Driver"] == driver]
            fig.add_trace(go.Bar(
                x=[driver],  # Ökumenn á X-ás
                y=driver_data["Points"],  # Points gildi á Y-ás
                name=driver
            ))

        # Uppsetning lóðrétta súluritsins
        fig.update_layout(
            title="Total Points in 2021 Season",
            xaxis_title="Driver",
            yaxis_title="Points",
            barmode="group",
            height=400,
            yaxis=dict(range=[350, 400]),  # Breyta hámarks gildi á Y-ás
            legend_title="Driver",
            template="plotly_white"
        )

        return fig

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
                    "width": "700px",  # Adjust the width as needed
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
            
    # Línurit fyrir uppsöfnuð stig
    @output
    @render_widget
    def hamilton_verstappen_cumulative_plot():
        # Sækja gögn fyrir uppsöfnuð stig
        query_points = """
            SELECT race_id, driver_id, race_points
            FROM hamilton_verstappen_race_data_2021
            WHERE type = 'RACE_RESULT'
        """
        data_points = pd.read_sql(query_points, con)

        # Sækja gögn fyrir sigurstaði
        query_wins = """
            SELECT race_id, driver_id, position_display_order
            FROM hamilton_verstappen_race_data_2021
            WHERE type = 'RACE_RESULT' AND position_display_order = 1
        """
        data_wins = pd.read_sql(query_wins, con)

        # Nota 'driver_id' sem inniheldur nöfnin beint
        data_points['driver'] = data_points['driver_id']
        data_wins['driver'] = data_wins['driver_id']

        # Reikna uppsafnaðan fjölda stiga fyrir hvern ökumann
        data_points['cumulative_points'] = data_points.groupby('driver')['race_points'].cumsum()

        # Fjarlægja NaN gildi ef einhver eru
        data_points = data_points.dropna(subset=['race_id', 'cumulative_points'])

        # Línurit fyrir uppsöfnuð stig
        fig = px.line(
            data_points, x="race_id", y="cumulative_points", color="driver", line_group='driver',
            title="Hamilton vs Verstappen: Uppsöfnuð Stig árið 2021",
            markers=True,
            color_discrete_map={
                'lewis-hamilton': 'blue',
                'max-verstappen': 'red'
            }
        )

        # Bæta stjörnum við sigurstaði fyrir Hamilton
        fig.add_trace(go.Scatter(
            x=data_wins[data_wins['driver'] == 'lewis-hamilton']['race_id'],
            y=data_points[data_points['driver'] == 'lewis-hamilton']['cumulative_points'].iloc[
                data_wins[data_wins['driver'] == 'lewis-hamilton']['race_id'].index] - 5,  # Færa stjörnu aðeins nær grafinu
            mode='markers',
            name='Hamilton Wins',
            marker=dict(symbol='star', size=12, color='blue')  # Minni stjörnur fyrir Hamilton
        ))

        # Bæta stjörnum við sigurstaði fyrir Verstappen
        fig.add_trace(go.Scatter(
            x=data_wins[data_wins['driver'] == 'max-verstappen']['race_id'],
            y=data_points[data_points['driver'] == 'max-verstappen']['cumulative_points'].iloc[
                data_wins[data_wins['driver'] == 'max-verstappen']['race_id'].index] - 5,  # Færa stjörnu aðeins nær grafinu
            mode='markers',
            name='Verstappen Wins',
            marker=dict(symbol='star', size=12, color='red')  # Minni stjörnur fyrir Verstappen
        ))

        # Uppfæra ása og útlit
        fig.update_layout(
            xaxis_title="Keppni",
            yaxis_title="Uppsöfnuð Stig",
            legend_title="Driver",
            template="plotly_white"
        )

        return fig


    # Línurit fyrir stöðu í keppnum
    @output
    @render_widget
    def hamilton_verstappen_position_plot():
    # Sækja gögn úr töflunni 'hamilton_verstappen_race_data_2021' með 'type' = 'RACE_RESULT'
        query = """
            SELECT race_id, driver_id, position_display_order
            FROM hamilton_verstappen_race_data_2021
            WHERE type = 'RACE_RESULT'
        """
        data = pd.read_sql(query, con)

        # Nota 'driver_id' sem inniheldur nöfnin beint
        data['driver'] = data['driver_id']

        # Gera ráð fyrir að 'race_id' og 'position_display_order' séu heiltölur
        data['race_id'] = data['race_id'].astype(int)
        data['position_display_order'] = data['position_display_order'].astype(int)

        # Raða gögnunum eftir ökumanni og keppni
        data = data.sort_values(['driver', 'race_id'])

        # Fjarlægja NaN gildi ef einhver eru
        data = data.dropna(subset=['race_id', 'position_display_order'])

        # Aðal línuritið fyrir stöðu í keppnum
        fig = px.line(
            data, x="race_id", y="position_display_order", color="driver", line_group='driver',
            title="Hamilton vs Verstappen: Staða í Keppnum árið 2021",
            markers=True,
            color_discrete_map={
                'lewis-hamilton': 'blue',
                'max-verstappen': 'red'
            }
        )

        # Finna gögn þar sem position_display_order = 1 (sigurvegari)
        winner_data = data[data['position_display_order'] == 1]

        # Bæta við stjörnum fyrir sigurvegara
        fig.add_trace(go.Scatter(
            x=winner_data[winner_data['driver'] == 'lewis-hamilton']['race_id'],
            y=winner_data[winner_data['driver'] == 'lewis-hamilton']['position_display_order'],
            mode='markers+text',
            name='Hamilton Wins',
            marker=dict(symbol='star', size=15, color='blue'),  # Blá stjarna fyrir Hamilton
        ))

        fig.add_trace(go.Scatter(
            x=winner_data[winner_data['driver'] == 'max-verstappen']['race_id'],
            y=winner_data[winner_data['driver'] == 'max-verstappen']['position_display_order'],
            mode='markers+text',
            name='Verstappen Wins',
            marker=dict(symbol='star', size=15, color='red'),  # Rauð stjarna fyrir Verstappen
        ))

        # Snúa y-ásnum svo 1. staður sé efst
        fig.update_yaxes(autorange="reversed")

        # Uppfæra ása og útlit
        fig.update_layout(
            xaxis_title="Keppni",
            yaxis_title="Staða í Keppni",
            template="plotly_white"
        )

        return fig
    
    # Nýir úttakshlutir fyrir framleiðenda frammistöðu
    @output
    @render_widget
    def manufacturer_average_points_plot():
        if input.manufacturer_type():
            manufacturer_column = manufacturer_choices[input.manufacturer_type()]
            # Sækja gögn úr 'race_result' viewinu
            query = f"""
                SELECT {manufacturer_column} AS manufacturer_id, points
                FROM race_result
            """
            data = pd.read_sql(query, con)
            # Hópa eftir framleiðanda og reikna meðaltal stiga
            average_points = data.groupby('manufacturer_id')['points'].mean().reset_index()
            # Sækja samanlögð stig til að sía út þá sem hafa minna en 100 stig
            total_points = data.groupby('manufacturer_id')['points'].sum().reset_index()
            # Tengja saman meðaltal og samtala
            merged_data = pd.merge(average_points, total_points, on='manufacturer_id', suffixes=('_mean', '_sum'))
            # Sía út þá sem hafa samtala stiga minna en 100
            filtered_data = merged_data[merged_data['points_sum'] >= 100]
            # Teikna súlurit fyrir meðaltal stiga
            fig = px.bar(
                filtered_data.sort_values('points_mean', ascending=False),
                x='manufacturer_id', y='points_mean',
                title=f"Meðaltal Stiga eftir {input.manufacturer_type()} (≥100 samtala stiga)"
            )
            fig.update_layout(xaxis_title=input.manufacturer_type(), yaxis_title="Meðaltal Stiga")
            fig.update_xaxes(tickangle=45)
            return fig

    @output
    @render_widget
    def manufacturer_total_points_plot():
        if input.manufacturer_type():
            manufacturer_column = manufacturer_choices[input.manufacturer_type()]
            # Sækja gögn úr 'race_result' viewinu
            query = f"""
                SELECT {manufacturer_column} AS manufacturer_id, points
                FROM race_result
            """
            data = pd.read_sql(query, con)
            # Hópa eftir framleiðanda og reikna samtala stiga
            total_points = data.groupby('manufacturer_id')['points'].sum().reset_index()
            # Sía út þá sem hafa samtala stiga minna en 100
            filtered_data = total_points[total_points['points'] >= 100]
            # Teikna súlurit fyrir samtala stiga
            fig = px.bar(
                filtered_data.sort_values('points', ascending=False),
                x='manufacturer_id', y='points',
                title=f"Samtala Stiga eftir {input.manufacturer_type()} (≥100 samtala stiga)"
            )
            fig.update_layout(xaxis_title=input.manufacturer_type(), yaxis_title="Samtala Stiga")
            fig.update_xaxes(tickangle=45)
            return fig
        
    # Sýna lóðrétt súlurit
    @output
    @render_widget
    def wins_bar_chart():
        # Gögnin fyrir Wins
        wins_data = pd.DataFrame({
            "Driver": ["Lewis Hamilton", "Max Verstappen"],
            "Wins": [hamilton_wins, verstappen_wins]  # Fastar tölur, getur breytt í breytur ef þær eru skilgreindar
        })

        # Plotly súlurit
        fig = go.Figure()

        # Bæta við súlum fyrir hvern ökumann
        for driver in wins_data["Driver"]:
            driver_data = wins_data[wins_data["Driver"] == driver]
            fig.add_trace(go.Bar(
                x=[driver],  # Ökumenn á X-ás
                y=driver_data["Wins"],  # Wins gildi á Y-ás
                name=driver,
                text=driver_data["Wins"],  # Texti sem birtir Wins beint á súlunum
                textposition="auto",  # Textinn birtist sjálfvirkt á réttum stað
            ))

        # Uppsetning lóðrétta súluritsins
        fig.update_layout(
            title="2021 Wins Comparison",
            xaxis_title="Driver",
            yaxis_title="Wins",
            barmode="group",  # Hópar saman súlur fyrir skýrleika
            height=400,
            legend_title="Driver",
            template="plotly_white"  # Hreint útlit
        )

        return fig
    
    @output
    @render_widget
    def horizontal_race_bar_chart():
        # Ná í valið keppni
        race = input.race_select()

        # Ná í gögn fyrir valda keppni
        df = get_race_points(race)
        
        # Búa til lóðrétt súlurit
        fig = px.bar(
            df,
            x="driver_id",
            y="race_points",
            title=f"Race Points for {race}",
            labels={"driver_id": "Driver", "race_points": "Points"},
            color="driver_id",  # Litir eftir keppanda
            color_discrete_map={
                'lewis-hamilton': 'rgba(0, 0, 255, 0.7)',  # Smooth blátt fyrir Hamilton
                'max-verstappen': 'rgba(255, 0, 0, 0.7)'   # Smooth rautt fyrir Verstappen
            }
        )
        fig.update_layout(
            xaxis_title="Driver",
            yaxis_title="Race Points",
            template="plotly_white",
            showlegend=False  # Fjarlægja legend ef ekki nauðsynlegt
        )
        return fig

    @output
    @render_widget
    def fastest_lap_chart_2():
        race_id = race_mapping.get(input.race_select())
        if not race_id:
            return go.Figure()

        query = f"""
        SELECT driver_id, MIN(lap_time) as fastest_lap
        FROM f1_race_data
        WHERE race_id = {race_id}
        GROUP BY driver_id
        """
        df = pd.read_sql_query(query, con)
        if df.empty:
            return go.Figure()

        fig = px.bar(
            df,
            x="driver_id",
            y="fastest_lap",
            title="Fastest Lap Comparison",
            labels={"driver_id": "Driver", "fastest_lap": "Lap Time (s)"},
            color="driver_id",
        )
        return fig
    
    @output
    @render_widget
    def horizontal_race_time_comparison_chart():
        # Fá valið keppni
        race_id = race_mapping.get(input.race_select())
        if not race_id:
            # Skila tómu grafi ef race_id er ekki gilt
            fig = go.Figure()
            fig.update_layout(
                title="No data available for the selected race.",
                xaxis_title="Race Time",
                yaxis_title="Driver",
                template="plotly_white"
            )
            return fig

        # SQL fyrirspurn til að ná í race_time fyrir hvern keppanda
        query = f"""
        SELECT driver_id, race_time
        FROM hamilton_verstappen_race_data_2021
        WHERE race_id = {race_id}
        """
        df = pd.read_sql_query(query, con)
        # Fjarlægja None eða óþekkt gildi í dálknum
        df = df.dropna(subset=["race_time"])

        df["race_time"] = df["race_time"].apply(convert_time_to_seconds)


        # Athuga hvort gögn séu til
        if df.empty:
            fig = go.Figure()
            fig.update_layout(
                title="No data available for the selected race.",
                xaxis_title="Race Time",
                yaxis_title="Driver",
                template="plotly_white"
            )
            return fig
        
        min_value = df["race_time"].min()
        max_value = df["race_time"].max()
        buffer = (max_value - min_value) * 0.25

        fig = px.bar(
            df,
            y="driver_id",
            x="race_time",
            orientation="h",
            title="Race Time Comparison",
            labels={"driver_id": "Driver", "race_time": "Race Time (s)"},
            color="driver_id",
            color_discrete_map={
                'lewis-hamilton': 'rgba(0, 0, 255, 0.7)',  # Smooth blátt fyrir Hamilton
                'max-verstappen': 'rgba(255, 0, 0, 0.7)'   # Smooth rautt fyrir Verstappen
            }
        )

        # Fínstilla x-ás
        min_value = df["race_time"].min()  # Minnsta gildið á x-ásnum
        fig.update_layout(
            xaxis=dict(
                title="Race Time (s)",
                range=[min_value - buffer, max_value + buffer],  # Lækka neðri mörk aðeins fyrir bil (2% minni)
            ),
            yaxis_title="Driver",
            template="plotly_white",
            showlegend=False
        )

        return fig
    
    @output
    @render_widget
    def vertical_comparison_barplot():
        # Fá valið keppni
        race_id = race_mapping.get(input.race_select())
        if not race_id:
            return go.Figure()

        # Fyrirspurn til að ná í race_points úr "hamilton_verstappen_race_data_2021"
        query_race_points = f"""
        SELECT driver_id, race_points, race_laps
        FROM hamilton_verstappen_race_data_2021
        WHERE race_id = {race_id}
        """
        df_race_points = pd.read_sql_query(query_race_points, con)

        # Fyrirspurn til að ná í laps og stops úr "race_data"
        query_race_data = f"""
        SELECT driver_id, stops
        FROM f1_race_data
        WHERE race_id = {race_id}
        GROUP BY driver_id
        """
        df_race_data = pd.read_sql_query(query_race_data, con)

        # Sameina gögnin í eina töflu
        df = pd.merge(df_race_points, df_race_data, on="driver_id", how="outer")

        # Umbreyta gögnunum í long-form fyrir samanburð á flokkum
        df_long = df.melt(
            id_vars=["driver_id"],  # Halda driver_id sem fastan dálk
            value_vars=["race_points", "race_laps", "stops"],  # Flokkarnir sem á að bera saman
            var_name="Category",  # Nafn dálks sem geymir flokkana
            value_name="Value"  # Nafn dálks sem geymir gildin
        )

        # Búa til lóðrétt súlurit
        fig = px.bar(
            df_long,
            x="driver_id",
            y="Value",
            color="Category",
            barmode="group",  # Hópar saman flokkum fyrir skýrleika
            title="Comparison of Race Points, Laps, and Stops",
            labels={"driver_id": "Driver", "Value": "Value", "Category": "Category"}
        )

        # Uppfæra útlit
        fig.update_layout(
            xaxis_title="Driver",
            yaxis_title="Value",
            template="plotly_white"
        )

        return fig
    
    
    @output
    @render_widget
    def horizontal_pit_stop_comparison_chart():
        # Fá valið keppni
        race_id = race_mapping.get(input.race_select())
        if not race_id:
            return go.Figure()

        # Fyrirspurn til að ná í pit_stop_time og pit_stop_time_sum úr gagnagrunninum
        query = f"""
        SELECT driver_id, 
            pit_stop_time, 
            pit_stop_time_sum
        FROM f1_race_data
        WHERE race_id = {race_id}
        """
        df = pd.read_sql_query(query, con)

        # Umbreyta 'pit_stop_time' og 'pit_stop_time_sum' með fallinu
        df['pit_stop_time'] = df['pit_stop_time'].apply(convert_time_to_seconds_2)
        df['pit_stop_time_sum'] = df['pit_stop_time_sum'].apply(convert_time_to_seconds_2)

        # Fjarlægja línur með NaN gildi eftir umbreytingu
        df = df.dropna(subset=['pit_stop_time', 'pit_stop_time_sum'])

        # Umbreyta gögnunum í long-form fyrir samanburð
        df_long = df.melt(
            id_vars=["driver_id"],  # Halda driver_id sem fastan dálk
            value_vars=["pit_stop_time", "pit_stop_time_sum"],  # Flokkarnir sem á að bera saman
            var_name="Category",  # Nafn dálks sem geymir flokkana
            value_name="Value"  # Nafn dálks sem geymir gildin
        )

        # Búa til lárétt súlurit
        fig = px.bar(
            df_long,
            y="driver_id",
            x="Value",
            color="Category",
            orientation="h",  # Lárétt súlurit
            barmode="group",  # Hópar saman flokkum fyrir skýrleika
            title="Comparison of Pit Stop Time and Total Pit Stop Time Sum",
            labels={"driver_id": "Driver", "Value": "Value (s)", "Category": "Category"}
        )

        # Uppfæra útlit: Stillir x-ásinn á rétt bil
        min_value = df_long["Value"].min()
        max_value = df_long["Value"].max()
        buffer = (max_value - min_value) * 0.1
        fig.update_layout(
            xaxis=dict(
                title="Value (s)",
                range=[min_value - buffer, max_value + buffer]  # Stillir bil á x-ás
            ),
            yaxis_title="Driver",
            template="plotly_white"
        )

        return fig

    
    @output
    @render_widget
    def fastest_lap_chart():
        # Fá valið keppni
        race_id = race_mapping.get(input.race_select())
        if not race_id:
            return go.Figure()

        # Fyrirspurn til að ná í hraðasta hringinn
        query = f"""
        SELECT driver_id, lap_time
        FROM f1_race_data
        WHERE race_id = {race_id}
        """
        df = pd.read_sql_query(query, con)

        # Umbreyta 'lap_time' í float, ólögleg gildi verða NaN
        df['lap_time'] = df['lap_time'].apply(convert_lap_time_to_seconds)

        # Fjarlægja línur með NaN
        df = df.dropna(subset=['lap_time'])

        # Ef engin gögn eru eftir, skila tómum grafinu
        if df.empty:
            fig = go.Figure()
            fig.update_layout(
                title="No valid data for the selected race.",
                xaxis_title="Lap Time (s)",
                yaxis_title="Driver",
                template="plotly_white"
            )
            return fig

        # Teikna graf
        fig = px.bar(
            df,
            y="driver_id",
            x="lap_time",
            orientation="h",
            title="Fastest Lap Comparison",
            labels={"driver_id": "Driver", "lap_time": "Lap Time (s)"},
            color="driver_id",
            color_discrete_map={
                'lewis-hamilton': 'rgba(0, 0, 255, 0.7)',
                'max-verstappen': 'rgba(255, 0, 0, 0.7)'
            }
        )

        # Stilla x-ás dynamic
        min_value = df["lap_time"].min()
        max_value = df["lap_time"].max()
        buffer = (max_value - min_value) * 0.25
        fig.update_layout(
            xaxis=dict(
                title="Lap Time (s)",
                range=[min_value - buffer, max_value + buffer]
            ),
            yaxis_title="Driver",
            template="plotly_white",
            showlegend=False
        )

        return fig
    
    @output
    @render_widget
    def start_vs_finish_positions_chart():
        # Fá valið keppni
        race_id = race_mapping.get(input.race_select())
        if not race_id:
            return go.Figure()

        # Fyrirspurn til að sækja gögn fyrir valda keppni
        query = f"""
        SELECT driver_id, 
            race_qualification_position_number, 
            race_grid_position_number, 
            race_positions_gained
        FROM hamilton_verstappen_race_data_2021
        WHERE race_id = {race_id}
        """
        df = pd.read_sql_query(query, con)

        # Hreinsa gögnin - tryggja að dálkar séu heiltölur
        df['race_qualification_position_number'] = pd.to_numeric(df['race_qualification_position_number'], errors='coerce')
        df['race_grid_position_number'] = pd.to_numeric(df['race_grid_position_number'], errors='coerce')
        df['race_positions_gained'] = pd.to_numeric(df['race_positions_gained'], errors='coerce')

        # Fjarlægja línur með NaN gildum
        df = df.dropna(subset=['race_qualification_position_number', 'race_grid_position_number', 'race_positions_gained'])

        # Búa til dálk fyrir endanlega stöðu byggða á ráslínustöðu + unnin sæti
        df['race_finish_position_number'] = df['race_grid_position_number'] - df['race_positions_gained']

        # Umbreyta í long-form til að búa til samanburð
        df_long = df.melt(
            id_vars=["driver_id"],  # Halda driver_id sem fastan dálk
            value_vars=[
                "race_qualification_position_number", 
                "race_grid_position_number", 
                "race_finish_position_number"
            ],
            var_name="Category",  # Nafn dálks sem geymir flokkana
            value_name="Position"  # Nafn dálks sem geymir stöðuna
        )

        # Teikna línurit
        fig = px.line(
            df_long,
            x="Category",
            y="Position",
            color="driver_id",
            markers=True,  # Sýna punkta fyrir hverja stöðu
            title="Starting vs Finishing Positions",
            labels={
                "driver_id": "Driver", 
                "Position": "Position (Lower is Better)", 
                "Category": "Category"
            },
            line_shape="linear",  # Bein lína á milli punkta
        )

        # Sérstill litina fyrir keppendur
        fig.update_traces(marker=dict(size=10))  # Stækka punktana fyrir skýrleika

        fig.update_layout(
            yaxis=dict(
                title="Position (Lower is Better)",
                autorange="reversed",  # Snúa ásnum þannig að lægsta gildi (besta staða) er efst
            ),
            xaxis_title="Category (Qualification, Grid, Finish)",
            template="plotly_white",
            legend_title="Driver"
        )

        return fig
    
    @output
    @render_widget
    def positions_gained_bar_chart():
        # Fá valið keppni
        race_id = race_mapping.get(input.race_select())
        if not race_id:
            return go.Figure()

        # Fyrirspurn til að sækja gögn fyrir valda keppni
        query = f"""
        SELECT driver_id, race_positions_gained
        FROM hamilton_verstappen_race_data_2021
        WHERE race_id = {race_id}
        """
        df = pd.read_sql_query(query, con)

        # Umbreyta í tölur og fjarlægja NaN gildi
        df['race_positions_gained'] = pd.to_numeric(df['race_positions_gained'], errors='coerce')
        df = df.dropna(subset=['race_positions_gained'])

        # Teikna lóðrétt bar chart
        fig = px.bar(
            df,
            x="driver_id",
            y="race_positions_gained",
            color="driver_id",
            title="Positions Gained or Lost",
            labels={
                "driver_id": "Driver",
                "race_positions_gained": "Positions Gained (+) or Lost (-)"
            },
            color_discrete_map={
                'lewis-hamilton': 'rgba(0, 0, 255, 0.7)',  # Blátt fyrir Hamilton
                'max-verstappen': 'rgba(255, 0, 0, 0.7)'   # Rautt fyrir Verstappen
            }
        )

        # Uppfæra y-ás fyrir jákvæð og neikvæð gildi
        min_value = df["race_positions_gained"].min()
        max_value = df["race_positions_gained"].max()
        buffer = (max_value - min_value)  # Gefa smá bil á ásnum
        
        # Bæta við þykkri núll-línu
        fig.add_shape(
            type="line",
            x0=-0.5,  # Byrjar aðeins fyrir utan fyrsta dálkinn
            x1=len(df['driver_id']) - 0.5,  # Eykur yfir alla dálka
            y0=0,
            y1=0,
            line=dict(
                color="black",
                width=4  # Þykkt núll-línu
            )
        )

        fig.update_layout(
            yaxis=dict(
                title="Positions Gained or Lost",
                range=[min_value - buffer, max_value + buffer]
            ),
            xaxis_title="Driver",
            template="plotly_white",
            showlegend=False  # Fjarlægja legend ef það er óþarfi
        )
        return fig

# Create the Shiny app
app = App(app_ui, server)
