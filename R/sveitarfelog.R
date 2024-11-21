library(shiny)
library(leaflet)
library(sf)
library(here)
library(dplyr)
library(lubridate)
library(readr)
library(scales)  

# Hlaða inn gögnum um fermetraverð með fasteignategund, ári og sveitarfélagi
sqm_data <- read_csv("data/heilbrigdisumdaemi/processed_kaupskra_per_sqm.csv")

# Skilgreina viðmót fyrir Shiny forritið
ui <- fluidPage(
  titlePanel("Sveitarfélög Íslands - Fermetraverð fyrir fasteignategundir"),
  sidebarLayout(
    sidebarPanel(
      sliderInput("year", "Veldu ár", min = min(sqm_data$year), max = max(sqm_data$year), value = max(sqm_data$year), sep = ""),
      selectInput("property_type", "Veldu fasteignategund",
                  choices = unique(sqm_data$property_type),
                  selected = "Fjölbýli")
    ),
    mainPanel(
      leafletOutput("map")
    )
  )
)

server <- function(input, output, session) {
  # Hlaða inn shapefile og undirbúa það
  d <- st_read(here("data-raw", "sveitarfelog", "Sveitarfelog_timalina.shp"),
               options = "ENCODING=ISO-8859-10") |>
    filter(endir_tima == max(endir_tima)) |>
    st_transform(crs = "WGS84")
  
  # Villuleit: Prenta sýnishorn af shapefile-gögnum til að tryggja að þau hlaðist inn
  print(head(d))
  
  output$map <- renderLeaflet({
    leaflet(d) |>
      addProviderTiles(providers$OpenStreetMap) |>
      addPolygons(
        weight = 2,
        opacity = 1,
        color = "blue",
        dashArray = "3",
        fillOpacity = 0.3,
        highlightOptions = highlightOptions(
          weight = 5,
          color = "#666",
          dashArray = "",
          fillOpacity = 0.7,
          bringToFront = TRUE
        ),
        label = ~ sveitarfel,
        labelOptions = labelOptions(
          style = list("font-weight" = "normal", padding = "3px 8px"),
          textsize = "15px",
          direction = "auto"
        )
      )
  })
  
  # Fylgjast með breytingum á ári og fasteignategund
  observe({
    selected_data <- sqm_data |>
      filter(year == input$year, property_type == input$property_type) |>
      select(sveitarfel, average_price_per_sqm)
    
    # Villuleit: Prenta sýnishorn af völdum gögnum
    print(head(selected_data))
    
    # Tengja valin gögn við shapefile gögn eftir sveitarfélagi
    d_selected <- left_join(d, selected_data, by = c("sveitarfel" = "sveitarfel"))
    
    # Villuleit: Prenta sýnishorn af tengdum gögnum til að tryggja að þau tengist rétt
    print(head(d_selected))
    
    # Uppfæra kort með völdum gögnum, meðhöndla N/A verð
    leafletProxy("map", data = d_selected) |>
      clearShapes() |>
      addPolygons(
        fillColor = ~ifelse(is.na(average_price_per_sqm), "lightgray", colorBin("YlOrRd", domain = d_selected$average_price_per_sqm, bins = 5)(average_price_per_sqm)),
        weight = 2,
        opacity = 1,
        color = "blue",
        dashArray = "3",
        fillOpacity = 0.5,
        label = ~paste(sveitarfel, "\n", 
                       "Fermetraverð: ", ifelse(is.na(average_price_per_sqm), "Gögn ekki tiltæk", paste0(comma(round(average_price_per_sqm)), " þúsund kr."))),
        labelOptions = labelOptions(
          style = list("font-weight" = "normal", padding = "3px 8px"),
          textsize = "15px",
          direction = "auto"
        )
      )
  })
}

# Keyra forritið
shinyApp(ui = ui, server = server)

