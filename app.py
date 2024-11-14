from shiny import App, ui, render
from shiny.types import ImgData
from pathlib import Path
import pandas as pd
import plotly.express as px

# Sample data for demonstration
def load_sample_data():
    data = pd.DataFrame({
        'Driver': ['Lewis Hamilton', 'Max Verstappen'],
        'Wins': [103, 50],
        'Podiums': [182, 85],
        'Poles': [103, 30]
    })
    return data

# Define ui
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
            ui.h3("Driver Statistics"),
            ui.output_table("driver_table")
        ),
        ui.nav_panel(
            "Bahrain",
            ui.h3("Performance Charts"),
            ui.output_plot("performance_chart")
        ),
        ui.nav_panel(
            "Emilia-Romagna",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Portugal",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Spain",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Monaco",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Azerbaijan",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "France",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Styria",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Austria",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Great Britain",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Hungary",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Belgium",
            ui.h3("Performance Charts"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Netherlands",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Italy",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Russia",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Turkey",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "United States",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Mexico",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Brazil",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Qatar",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Saudi Arabia",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        ),
        ui.nav_panel(
            "Abu Dhabi",
            ui.h3("About This Dashboard"),
            ui.p("This dashboard compares the statistics of Lewis Hamilton and Max Verstappen.")
        )

    )
)

# Define server logic
def server(input, output, session):
    # Load sample data
    data = load_sample_data()

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

    # Reactive text outputs
    @output
    @render.text
    def output_text():
        return f"You entered: {input.sample_input()}"

    @output
    @render.text
    def output_text_verbatim():
        return f"Slider value is: {input.sample_slider()}"

    # Render driver statistics table
    @output
    @render.table
    def driver_table():
        return data

    # Render performance chart
    @output
    @render.plot
    def performance_chart():
        fig = px.bar(
            data.melt(id_vars=['Driver'], var_name='Statistic', value_name='Value'),
            x='Statistic',
            y='Value',
            color='Driver',
            barmode='group',
            title='Driver Performance Comparison'
        )
        return fig

# Create the Shiny app
app = App(app_ui, server)
