from shiny import App, ui, render
from shiny.types import ImgData
from pathlib import Path
import pandas as pd
import plotly.express as px
import sqlite3


# Helper Functions
def snake_to_title(snake_str):
    """
    Converts snake_case string to Title Case with spaces.

    Args:
        snake_str (str): The snake_case string.

    Returns:
        str: The Title Case string with spaces.
    """
    components = snake_str.split('_')
    return ' '.join(x.capitalize() for x in components)


def clean_column_data(df, columns):
    """
    Removes dashes, dots, and commas from specified columns in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to clean.
        columns (list): List of column names to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
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

# Database path
db_path = '/Users/haatlason/Documents/GitHub/sqlite-greyjoy/capstone-ironislands/f1db.db'


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
    """
    Retrieves and processes head-to-head comparison data for Lewis Hamilton and Max Verstappen
    for a specific race.

    Args:
        race_id (int): The ID of the race.
        race_name (str): The name of the race.

    Returns:
        pd.DataFrame or None: A DataFrame containing the comparison data or None if no data found.
    """
    # SQL query to retrieve the filtered race data for the given race_id
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
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        return None

    # Rename 'position_display_order' to 'position display order'
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
            ui.layout_sidebar(
                ui.sidebar(
                    ui.input_text("sample_input", "Enter text:", placeholder="Type something here..."),
                    ui.input_slider("sample_slider", "Select a number:", min=0, max=100, value=50),
                ),
                # Main content area
                ui.div(
                    ui.h3("Overview Content"),
                    ui.output_text("output_text"),
                    ui.output_text_verbatim("output_text_verbatim")
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
        img: ImgData = {
            "src": str(img_path),
            "width": "200px",
            "height": "200px",
            "style": "border:5px solid Turquoise;"
        }
        return img

    # Render the Verstappen image
    @output
    @render.image
    def verstappen_image():
        img_path = Path(__file__).parent / "www" / "verstappen.jpeg"
        img: ImgData = {
            "src": str(img_path),
            "width": "200px",
            "height": "200px",
            "style": "border:5px solid blue;"
        }
        return img

    # Render the F1 logo image
    @output
    @render.image
    def f1logo_image():
        img_path = Path(__file__).parent / "www" / "f1logo.png"
        img: ImgData = {
            "src": str(img_path),
            "width": "120px",
            "height": "120px",
            "style": "border:2px solid white;"
        }
        return img

    # Reactive text outputs for "All-time Comparison" tab
    @output
    @render.text
    def output_text():
        return f"You entered: {input.sample_input()}"

    @output
    @render.text
    def output_text_verbatim():
        return f"Slider value is: {input.sample_slider()}"

    # Reactive output for race content in "2021 Season Comparison" tab
    @output
    @render.ui
    def race_content():
        race = input.race_select()
        if race == "2021 Season Overview":
            # Display the driver statistics table
            return ui.TagList(
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
                    "style": "display: block; margin-left: auto; margin-right: auto;"
                }
                return img
            else:
                # Optionally, return a default image or an error message
                # Here, returning an alt text
                return {
                    "src": "",
                    "alt": f"Image for {race} not found."
                }


# Create the Shiny app
app = App(app_ui, server)
