from shiny import App, render, ui
import pandas as pd
import plotly.express as px
import sqlite3
from shinywidgets import render_widget, output_widget

# Setja upp tengingu við gagnagrunn
con = sqlite3.connect("f1db.db")

# Lesa möguleika fyrir dropdown valmöguleika
driver_choices = pd.read_sql("SELECT name FROM driver", con)['name'].tolist()
constructor_choices = pd.read_sql("SELECT name FROM constructor", con)['name'].tolist()
circuit_choices = pd.read_sql("SELECT name FROM circuit", con)['name'].tolist()

# UI hluti
app_ui = ui.page_fluid(
    ui.h2("Formula 1 Mælaborð"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select("driver", "Veldu Ökumann", choices=driver_choices),
            ui.input_select("constructor", "Veldu Lið", choices=constructor_choices),
            ui.input_select("circuit", "Veldu Braut", choices=circuit_choices),
            ui.input_action_button("update", "Uppfæra")
        ),
        ui.page_auto(
            ui.navset_tab(
                ui.nav_panel("Ökumannsframmistaða", output_widget("driver_performance_plot")),
                ui.nav_panel("Liðsframmistaða", output_widget("constructor_performance_plot")),
                ui.nav_panel("Brautaframmistaða", output_widget("circuit_plot"))
            )
        )
    )
)

# Server hluti
def server(input, output, session):
    @output
    @render_widget
    def circuit_plot():
        if input.circuit():
            circuit_query = f"""
                SELECT race.id AS race_id, driver.name AS driver, race_driver_standing.points AS points 
                FROM race 
                JOIN circuit ON circuit.id = race.circuit_id 
                JOIN race_driver_standing ON race.id = race_driver_standing.race_id 
                JOIN driver ON driver.id = race_driver_standing.driver_id 
                WHERE circuit.name = '{input.circuit()}'
            """
            circuit_data = pd.read_sql(circuit_query, con)
            fig = px.line(
                circuit_data, x="race_id", y="points", color="driver",
                title=f"Frammistaða eftir Braut: {input.circuit()}"
            )
            fig.update_layout(xaxis_title="Keppni", yaxis_title="Stig")
            return fig  # Skila Plotly myndinni beint

    # Bættu við öðrum föllum fyrir ökumanns- og liðsframmistöðu á sama hátt
    @output
    @render_widget
    def driver_performance_plot():
        if input.driver():
            driver_query = f"""
                SELECT race.id AS race_id, race_driver_standing.points AS points 
                FROM race_driver_standing
                JOIN driver ON driver.id = race_driver_standing.driver_id
                JOIN race ON race.id = race_driver_standing.race_id
                WHERE driver.name = '{input.driver()}'
            """
            driver_data = pd.read_sql(driver_query, con)
            fig = px.line(
                driver_data, x="race_id", y="points",
                title=f"Frammistaða Ökumanns: {input.driver()}"
            )
            fig.update_layout(xaxis_title="Keppni", yaxis_title="Stig")
            return fig

    @output
    @render_widget
    def constructor_performance_plot():
        if input.constructor():
            constructor_query = f"""
                SELECT race.id AS race_id, race_constructor_standing.points AS points 
                FROM race_constructor_standing
                JOIN constructor ON constructor.id = race_constructor_standing.constructor_id
                JOIN race ON race.id = race_constructor_standing.race_id
                WHERE constructor.name = '{input.constructor()}'
            """
            constructor_data = pd.read_sql(constructor_query, con)
            fig = px.line(
                constructor_data, x="race_id", y="points",
                title=f"Frammistaða Liðs: {input.constructor()}"
            )
            fig.update_layout(xaxis_title="Keppni", yaxis_title="Stig")
            return fig

# Búa til Shiny appið
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
