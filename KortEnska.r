# Hlaða inn nauðsynlegum pökkum
# install.packages("tidyverse")
# install.packages("sf")
# install.packages("leaflet")

library(tidyverse)   # Fyrir gagnavinnslu og read_csv
library(sf)          # Fyrir landfræðileg gögn (Simple Features)
library(leaflet)     # Fyrir gagnvirk kort

Stadiums_data <- read_csv("/Users/ingvaratliaudunarson/Documents/GitHub/capstone-thereach/stadiumspremier.csv")


Stadiums_data <- Stadiums_data %>%
  mutate(Logo_url = paste0("/Users/ingvaratliaudunarson/Documents/GitHub/capstone-thereach/Logos/", str_replace_all(Team, " ", "_"), ".png"))

Location_data <- st_as_sf(Stadiums_data, coords = c("Longitude", "Latitude"), crs = 4326)

leaflet() %>%
  addTiles() %>%
  
  addMarkers(data = Location_data,
             lng = ~st_coordinates(geometry)[, 1],
             lat = ~st_coordinates(geometry)[, 2],
             icon = ~icons(iconUrl = Logo_url, iconWidth = 30, iconHeight = 30), 
             popup = ~paste("<b>Team:</b>", Team, "<br><b>Stadium:</b>", Stadium, "<br><b>City:</b>", City,"<br><b>Capacity:</b>",Capacity))
