from shiny import App, ui, render
import sqlite3
import pandas as pd

# Function to get a list of tables in the database
def get_table_names(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return [table[0] for table in tables]

# Function to fetch data from a specific table
def get_table_data(db_path, table_name):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

# Path to the database
DB_PATH = "f1db.db"

# Get the list of tables
table_names = get_table_names(DB_PATH)

# Define the UI
app_ui = ui.page_fluid(
    ui.h2("F1 Gagnagrunnur"),
    ui.navset_tab(
        # First tab (current content)
        ui.nav_panel(
            "Heim",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.input_text("sample_input", "Sláðu inn texta:", placeholder="Sláðu eitthvað hér..."),
                    ui.input_slider("sample_slider", "Veldu tölu:", min=0, max=100, value=50),
                ),
                ui.div(
                    ui.output_text("output_text"),
                    ui.output_text_verbatim("output_text_verbatim")
                )
            )
        ),
        # New tab to view database tables
        ui.nav_panel(
            "Skoða Gagnagrunn",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.input_select("selected_table", "Veldu töflu:", choices=table_names)
                ),
                ui.output_table("table_display")
            )
        )
    )
)

# Define the server logic
def server(input, output, session):
    # Server logic for the first tab
    @output
    @render.text
    def output_text():
        return f"Þú slóst inn: {input.sample_input()}"

    @output
    @render.text
    def output_text_verbatim():
        return f"Talan valin er: {input.sample_slider()}"

    # Server logic for the new tab to display tables
    @output
    @render.table
    def table_display():
        table_name = input.selected_table()
        if table_name:
            df = get_table_data(DB_PATH, table_name)
            return df
        return pd.DataFrame()

# Create the Shiny app
app = App(app_ui, server)
