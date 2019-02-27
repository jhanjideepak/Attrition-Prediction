rm(list = ls())#removes all objects from the current workspace

#Loading required packages
library(shiny)
library(dplyr)
library(magrittr)
library(ggplot2)
library(markdown)
library(scales)
library(shinyWidgets)
library(shinydashboard)
library(rjson)
library(jsonlite)
library(httr)
library(DT)
library(tidyr)
library(stringr)
library(shinyjs)


#Reading Dashboard data
json_file1 <<- "http://34.73.166.192/GetDashboardData"
df_hr1<-fromJSON(json_file1)


#reading Historical Data
json_file2 <<- "http://34.73.166.192/GetHistoricalData"
df_hr<-fromJSON(json_file2)

#End of file