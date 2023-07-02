# Load required packages
library(sp)
library(raster)
library(readr)
library(readxl)
library(sf)
library(maps)
library(spData)
library(magick)
library(grid)
library(tmaptools)
library(tmap)
library(tmapoptions)
library(viridisLite)
library(viridis)
library(tigris)
library(dplyr)
library(skimr)
library(tidyverse)
library(ggplot2)
# Load data
country_data <- read_sf("/home/adzavon/Documents/MSC_Data_Analysis/map_for conflicts/New_shapefile_to_use.shp")
conflict_categories = read_sf("/home/adzavon/Documents/MSC_Data_Analysis/map_for conflicts/conflicts_categories.shp")

colnames(country_data)
colnames(conflict_categories)
# # Static map with tmap - fill map
# tm_shape(country_data) +
#   tm_fill()
# 
# # Static map with tmap - contour map
# tm_shape(country_data) +
#   tm_borders()
# 
# # Static map with tmap - fill and contour map
# tm_shape(country_data) +
#   tm_polygons()
# 
# # Multiple maps with color
# t1 <- tm_shape(country_data) +
#   tm_fill(col = "aquamarine")
# t2 <- tm_shape(country_data) +
#   tm_fill(col = "aquamarine", alpha = 0.5)
# t3 <- tm_shape(country_data) +
#   tm_polygons(col = "aquamarine", border.col = "darkolivegreen")
# t4 <- tm_shape(country_data) +
#   tm_borders(lwd = 2)
# t5 <- tm_shape(country_data) +
#   tm_borders(lty = 4)
# t6 <- tm_shape(country_data) +
#   tm_polygons(col = "#E2E2E2", border.alpha = 0.5, lwd = 3)
# tmap_arrange(t1, t2, t3, t4, t5, t6, ncol = 3)
# 
# # Only one map with fill color based on SUM_CONFLICTS
# tm_shape(country_data) +
#   tm_polygons(col = "SUM_CONFLI", palette = "viridis", midpoint = 0)
# tm_shape(country_data)+
#   tm_polygons(col = "SUM_CONFLI") +
#   tm_style("classic")
# country_data <- st_as_sf(country_data)



#  The final map
tmapoptions(width = 8, height = 6)

tm_shape(country_data,
         style="quantile", 
         palette=get_brewer_pal(palette="OrRd", n=5, plot=FALSE))+
  tm_polygons(
    col = "SUM_CONFLI",
    style = "cont",
   # pal = viridis(8, direction = -1),
    title = "Conflicts Level"
  ) +
  tm_facets(by = c("Year","EVENT_TYPE"), ncol = 2)+
  tm_layout(main.title = "Cnflicts Events by Year", title.size = 1, 
          title.position = c("left", "top"), 
          legend.outside=FALSE, legend.position= c(.01, .1))+
 tm_layout(legend.outside.size = 3)+
 #tm_scale_bar(position = c("right", "bottom"))+
 tm_compass(position = c("right", "top"), size = 2)+
  tm_layout(legend.bg.color = "grey90", legend.bg.alpha=0.1, legend.frame=FALSE)+
  tm_scale_bar(position=c(0.6, 0.1),breaks = c(0, 125, 250), text.size=1) +
  tm_layout(title.size = 5, legend.text.size = 2, legend.title.size = 3,legend.outside=FALSE)
 




tmapoptions(width = 8, height = 6)

tm_shape(conflict_categories,
         style="quantile", 
         palette=get_brewer_pal(palette="OrRd", n=5, plot=FALSE))+
  tm_polygons(
    col = "SUM_CONFLI",
    style = "cont",
    # pal = viridis(8, direction = -1),
    title = "Conflicts Level"
  ) +
  tm_facets(by = c("Year","EVENT_TYPE"), ncol = 2 ,scale.factor = 10)+
  tm_layout(main.title = "Conflicts Events by Year (2018-2022)", title.size = 1, 
            title.position = c("left", "top"), 
            legend.outside=FALSE, legend.position= c(.01, .1))+
  tm_layout(legend.outside.size = 30)+
  #tm_scale_bar(position = c("right", "bottom"))+
  tm_compass(position = c("right", "top"), size = 2)+
  tm_layout(legend.bg.color = "grey90", legend.bg.alpha=0.1, legend.frame=FALSE)+
  tm_scale_bar(position=c(0.6, 0.00),breaks = c(0, 125, 250), text.size=1) +
  tm_layout(title.size = 5, legend.text.size = 2, legend.title.size = 3,legend.outside=FALSE, main.title.position ='center')

