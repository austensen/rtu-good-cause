library(tidyverse)
library(glue)
library(fs)
library(sf)
library(htmlwidgets)
library(htmltools)
library(leaflet)
library(leafpop)
library(leaflet.mapboxgl) # remotes::install_github("rstudio/leaflet.mapboxgl")
library(dotenv)


# Setup -------------------------------------------------------------------

# Edit ".env_sample" to set variables and save as ".env"
load_dot_env(".env")

# Free to sign up for API key here: https://account.mapbox.com/auth/signup/
options(mapbox.accessToken = Sys.getenv("MAPBOX_TOKEN"))


# Prep Data ---------------------------------------------------------------

pluto <- read_csv(path("data-raw", "pluto-extract.csv"), col_types = "ccciddd")

nopv <- read_csv(path("data-clean", "dof-nopv-20210115.csv"), col_types = "cl")

star_bbls <- nopv %>%
    mutate(star = if_else(is.na(star) & str_detect(bbl, ".*75\\d{2}$"), FALSE, star)) %>%
    filter(star)


target_bbls <- pluto %>%
    anti_join(star_bbls, by = "bbl") %>%
    st_as_sf(coords = c("longitude", "latitude")) %>%
    transmute(
        address = glue("{address}, {zipcode}"),
        dap_portal = glue("<a href=https://portal.displacementalert.org/property/{bbl}>DAP Portal<a>"),
        bbl,
        units = unitsres,
        floors = numfloors,
        zipcode
    )


# Make Maps ---------------------------------------------------------------

make_map <- function(zip) {

  map_bbls <- target_bbls %>%
    filter(zipcode == zip)

  map_title <- tags$div(
    HTML(glue("<h3>Good Cause Outreach Properties ({zip})</h3>"))
  )

  popup <- popupTable(
    map_bbls,
    c("address", "dap_portal", "bbl", "units", "floors"),
    row.numbers = FALSE,
    feature.id = FALSE
  )

  map <- map_bbls %>%
    leaflet() %>%
    addMapboxGL(style = "mapbox://styles/mapbox/light-v9") %>%
    addControl(map_title, position = "topright") %>%
    addCircleMarkers(
      fillOpacity = 0.6,
      color = "red",
      weight = 0,
      radius = 2,
      opacity = 0.8,
      popup = popup
    )

  saveWidget(map, file = path("docs", glue("{zip}.html")))

}

make_map("11385")
make_map("11378")
make_map("11379")
