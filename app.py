from shiny import App, ui, render
import sqlite3
import pandas as pd
from shinywidgets import output_widget, render_widget
import plotly.graph_objects as go
import numpy as np
import plotly.express as px


# Path to the database
DB_PATH = "f1db.db"

# Function to fetch data from the table and calculate statistics
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

# Get stats for Hamilton and Verstappen
hamilton_original = get_driver_stats("lewis-hamilton")
verstappen_original = get_driver_stats("max-verstappen")

# Skala gögnin á kvarðann 0-100 fyrir grafin
def scale_to_log(data):
    data = np.log(data)
    return data

# Skala gögnin fyrir plottið
hamilton_values_scaled = scale_to_log(hamilton_original.values)
verstappen_values_scaled = scale_to_log(verstappen_original.values)

categories = ['Total Points', 'Fastest Laps', 'Positions Gained', 'Driver of the Day Awards', 'Grand Slams']
categoriesSpider = ['Total Points', 'Fastest Laps', 'Positions Gained', 'Driver of the Day Awards', 'Grand Slams']

# Finna vísitölur fyrir þá flokka sem eru í categoriesSpider
indices = [categories.index(cat) for cat in categoriesSpider]

# Leggja saman einungis þá flokka sem eru í categoriesSpider fyrir hvorn keppanda
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
            radialaxis=dict(visible=True, range=[0,10])  # Set range to 0-100 after scaling
        ),
        showlegend=True
    )
    
    return fig


# Function to fetch cumulative points progression data from the table
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

# Create the points progression line chart with dynamic x-axis
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
        marker=dict(color='gold', size=5, symbol='star'),
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
        marker=dict(color='gold', size=5, symbol='star'),
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

# Function to fetch fastest lap times data from the table
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

# Get fastest lap data for both drivers
fastest_lap_data = get_fastest_lap_data()

# Process data for heatmap
def prepare_heatmap_data(df):
    # Pivot data to have drivers as rows, race_id as columns, and lap times as values
    heatmap_data = df.pivot(index="driver_id", columns="race_id", values="fastest_lap_time_millis")
    
    heatmap_data = heatmap_data.fillna(0)
    return heatmap_data


# Create the fastest lap heatmap
def create_fastest_lap_heatmap():
    # Prepare data
    heatmap_data = prepare_heatmap_data(fastest_lap_data)
    drivers = heatmap_data.index.tolist()  # Driver names (rows)
    races = heatmap_data.columns.tolist()  # Race IDs (columns)
    z_values = heatmap_data.values         # Lap times for each driver and race
    
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

# Function to fetch location and performance data
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
    
    # Fylla út NaN gildi í race_points með 0
    df['race_points'] = df['race_points'].fillna(0)
    
    return df

# Útfærir meðaltalsstig yfir allan tímann fyrir hverja staðsetningu
def get_average_points(data):
    avg_data = data.groupby(['circuit_id', 'lat', 'lon', 'driver_id']).race_points.mean().reset_index()
    avg_data.rename(columns={'race_points': 'avg_points'}, inplace=True)
    return avg_data

# Búa til kort með meðaltalsgögnum
def create_performance_map(data):
    # Nota meðaltalsstig
    data = get_average_points(data)
    
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
        mapbox_style="light",  # Þú getur valið annan stíl eins og "satellite-street"
        zoom=1,
        height=600
    )
    
    #fig.update_geos(
     #   showcoastlines=True, 
      #  coastlinecolor="Black", 
       # projection_type="azimuthal equal area"
    #)
    
    #fig.update_layout(
     #   margin={"r":0,"t":40,"l":0,"b":0},
      #  legend_title="Driver"
    #)
    fig.update_layout(mapbox=dict(accesstoken="pk.eyJ1IjoiYnJ5bmphcjgiLCJhIjoiY20zZzRxcGdtMDB0NDJtczZ1NWQwcGdqcyJ9.R0R4d1jbGxe9ZC0ydvT7gQ"))
    return fig

# Sækir gögnin og býr til meðaltalskortið
location_performance_data = get_location_and_performance_data()

# Define Shiny UI and server
app_ui = ui.page_navbar(  
    ui.nav_panel("Overview", ui.h2("Lewis Hamilton VS Max Verstappen Overview"),
                 ui.page_fillable(
                     ui.layout_columns(
                         ui.card(ui.h3("Log-skalað Spider Chart"), 
                            ui.layout_columns(
                                ui.card(
                                    ui.h4("Spider Chart"), 
                                    output_widget("spider_chart")
                                ),
                                ui.layout_column_wrap(
                                    ui.card(
                                        ui.h5("Lewis Hamilton log-sköluð summa"),
                                        ui.p(f"{hamilton_logSpider_sum:.2f}")
                                    ),
                                    ui.card(
                                        ui.h5("Max Verstappen log-sköluð summa"),
                                        ui.p(f"{verstappen_logSpider_sum:.2f}")
                                    ),
                                    col_width=6
                                ),
                                col_widths=[12, 4],
                            )
                        ),
                         ui.card(ui.h3("Stig yfir tíma"),
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
                                            ui.h5("Lewis Hamilton sigrar"),
                                            ui.p(f"{hamilton_wins:.0f}")
                                            ),
                                        ui.card(
                                            ui.h5("Max Verstappen sigrar"),
                                            ui.p(f"{verstappen_wins:.0f}")
                                            ),
                                        ),
                                col_widths=[12, 4, 4]
                                )
                            ),
                         ui.card(ui.h3("Hitakort yfir hröðustu umferðir"),
                             output_widget("fastest_lap_heatmap")
                             ),
                         ui.card(ui.h3("Kort af keppnisstöðum með frammistöðu"),
                                 output_widget("performance_map")
                         ),
                         col_widths=[12, 12, 12],
                         )
                     )
                 ),  
    ui.nav_panel("2021", "Lewis Hamilton VS Max Verstappen 2021"),   
    title="Lewis Hamilton VS Max Verstappen",  
    id="page",  
)  
def server(input, output, session):
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
        # Birta einungis meðaltalskortið
        return create_performance_map(location_performance_data)

app = App(app_ui, server)