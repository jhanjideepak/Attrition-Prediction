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

dashboardPage(skin = "blue",
              dashboardHeader(title = "HR Analytics - Attrition Predictor"),
              dashboardSidebar(
                
                actionButton("about","About"),
                actionButton("show1","Instructions to Upload File")
                
                
                
              ),# end of dashboardSidebar
              dashboardBody(
                tags$style(type="text/css",
                           ".shiny-output-error { visibility: hidden; }",
                           ".shiny-output-error:before { visibility: hidden; }"
                ),
                fluidRow(
                  tabBox(width = 12, height = NULL,
                        tabPanel("Dashboard",value=1,
                            fluidRow(
                              
                              column(width = 6,  box(title = "Current Attrition Rate", width = NULL, solidHeader = FALSE, plotOutput("Plot11"))),
                              column(width = 6,  box(title = "Age Grouped by Attrition ", width = NULL, solidHeader = FALSE, plotOutput("Plot12"))),
                              column(width = 6,  box(title = "Monthly Income Grouped by Attrition", width = NULL, solidHeader = FALSE, plotOutput("Plot13"))),
                              column(width = 6,  box(title = "NumCompaniesWorked Grouped by Attrition", width = NULL, solidHeader = FALSE, plotOutput("Plot14"))),
                              column(width = 6,  box(title = "YearsSinceLastPromotion Grouped by Attrition", width = NULL, solidHeader = FALSE, plotOutput("Plot15"))),
                              column(width = 6,  box(title = "DistanceFromHome Grouped by Attrition", width = NULL, solidHeader = FALSE, plotOutput("Plot16")))
                              
                              
                            )),
                        tabPanel("Historical Data",value=2,
                           
                             fluidRow(
                      
                            column(width = 4,  box(title = "Upload File", width = NULL, solidHeader = FALSE, fileInput("file1", "Choose a csv file to upload:",accept = c("text/csv", "text/comma-separated-values, text/plain", ".csv")))),
                              tabsetPanel(
                              id="dataset",
                             
                              tabPanel(
                                "Plot",
                                
                                h4("Select employees of attrition or non-attrition to visualize."),
                                
                                checkboxGroupInput(
                                  "att_vars",
                                  "Attrition or not:",
                                  c("Yes", "No"),
                                  selected=c("Yes", "No")),
                                
                                fluidRow(
                                  
                                  column(
                                    4, 
                                    h4("Count of discrete variable."),
                                    plotOutput("plot3"),
                                    
                                    checkboxGroupInput(
                                      "disc_vars",
                                      "Job roles:",
                                      unique(df_hr$JobRole),
                                      selected=unique(df_hr$JobRole)[1:5])
                                  ),
                                  
                                  column(
                                    4, 
                                    h4("Distribution of continuous variable."),
                                    plotOutput("plot"),
                                    
                                    selectInput(
                                      "plot_vars",
                                      "Variable to visualize:",
                                      names(select_if(df_hr, is.integer)),
                                      selected=names(select_if(df_hr, is.integer)))
                                  ),
                                  
                                  column(
                                    4, 
                                    h4("Comparison on certain factors."),
                                    plotOutput("plot2"),
                                    
                                    # Years of service.
                                    
                                    sliderInput(
                                      "years_service",
                                      "Years of service:",
                                      min=1,
                                      max=40,
                                      value=c(2, 5)),
                                    
                                    # Job level.
                                    
                                    sliderInput(
                                      "job_level",
                                      "Job level:",
                                      min=1,
                                      max=5,
                                      value=3
                                    ),
                                    
                                    checkboxGroupInput(
                                      "job_roles",
                                      "Job roles:",
                                      unique(df_hr$JobRole),
                                      selected=unique(df_hr$JobRole)[1:5]),
                                    
                                    column(3, actionButton("showTab", "Retrain the Model", icon("paper-plane"), 
                                                           style="color: #fff; background-color: #337ab7; border-color: #2e6da4"))
                                    
                                  )
                                )
                              ),
                              tabPanel("Analysis", "Result after running classification model",
                                       column(3, actionButton("retrain", "Retrain the model", 
                                                              style="color: #fff; background-color: #337ab7; border-color: #2e6da4")))
                              
                            )
                              )),
                        tabPanel("New Data",value=3,
                              fluidRow(
                                column(width = 4,  box(title = "Upload File", width = NULL, solidHeader = FALSE, fileInput("file2", "Upload data for prediction",accept = c("text/csv", "text/comma-separated-values, text/plain", ".csv")))),
                                column(width = 6, actionButton("runpred","Make Prediction") ),
                                column(width = 6, actionButton("runsurvival","Survival Anlysis") )),
                              tabsetPanel(id="dataset1",
                                tabPanel("HR Demographic data",value=4,
                                fluidRow(
                                column(width = 6, DT::dataTableOutput("newhrdata")))),
                               tabPanel("Survival Analysis",
                                       fluidRow(
                                          column(width = 8,  box(title = "Pred", width = NULL, solidHeader = FALSE, DT::dataTableOutput("surivalprediction")),downloadButton("downloadData1", "Download Predictions"))
                                        )),
                                tabPanel("Attrition Prediction",
                                    fluidRow(
                                      column(width = 8,  box(title = "Pred", width = NULL, solidHeader = FALSE, DT::dataTableOutput("attritionprediction")),downloadButton("downloadData", "Download Predictions"))
                                )))
                              )))#End of first fluidRow
                             )#end of dashboard body
                            )#end of dashboard page

