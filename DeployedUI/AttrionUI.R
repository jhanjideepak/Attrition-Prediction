source("global.R")


#UI Code
ui<-dashboardPage(skin = "blue",#Dashboard started
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
                         tabPanel("Explore Data",value=2,
                                  
                                  fluidRow(
                                    
                                    #column(width = 4,  box(title = "Upload File", width = NULL, solidHeader = FALSE, fileInput("file1", "Choose a csv file to upload:",accept = c("text/csv", "text/comma-separated-values, text/plain", ".csv")))),
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
                                      tabPanel("Analysis", "Done"
                                      )
                                      
                                    )
                                  )),
                         tabPanel("Get Prediction",value=3,
                                  fluidRow(
                                    column(width = 4,  box( width = NULL, solidHeader = FALSE, fileInput("file2", "Please upload the data before making prediction",accept = c("text/csv", "text/comma-separated-values, text/plain", ".csv")))),
                                    useShinyjs(),
                                    column(width = 6, actionButton("runpred","Make Prediction") ),
                                    column(width = 6, actionButton("runsurvival","Survival Anlysis") )),
                                  tabsetPanel(id="dataset1",
                                              tabPanel("View Data",value=4,
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




server<-function(input,output,session) {
  #===============================================================================#
  #                        DASHBOARD SERVER FUNCTIONS                            #
  #===============================================================================#
 
  #Read new data to make prediction
  filedata <-reactive({
    inFile <<- input$file2
    if (is.null(inFile))
    {
      return(NULL)
    }
    forpred<<-read.csv(inFile$datapath, header = TRUE)
    return(forpred)
  })
  
  
  
  #Showing new data on the UI
  output$newhrdata<-DT::renderDataTable({
    inFile <<- input$file2
    if (is.null(inFile))
    {
      return(NULL)
    }
    forpred<<-read.csv(inFile$datapath, header = TRUE)
    datatable(forpred)
  })
  
  
  
  #Showing prediction on the UI 
  output$attritionprediction<-DT::renderDataTable({
    app1},options = list(scrollX = TRUE))
  
  #Showing New tab
  observeEvent(input$showTab, {
    showTab(inputId = "tabs", target = "Analysis")
  })
  
  #Updating Tab
  observeEvent(input$showTab, {
    updateTabsetPanel(session, "dataset",selected = "Analysis")
  })
  
  
  #Retraining the prediction model
  observeEvent(input$showTab,{
    json_file1 <- "http://34.73.166.192/GetHistoricalData"
    retraindf<-fromJSON(json_file1)
    retrain <- POST("http://34.73.166.192/RetrainAttritionPredictionModel"
                    , body = retraindf
                    , encode = "json")
    appData1 <<- content(retrain,"text")
    h=data.frame(as.list(appData1))
    if(h=="Success")
      print("Retrained the model")
    else
      print("Failed")
  })
  
  
  
  
  #Getting attrition prediction
  observeEvent(input$runpred, {
    
    if(exists("forpred")){
    showTab(inputId = "tabs", target = "Attrition Prediction")
      res <- POST("http://34.73.166.192/GetAttritionPrediction1"
                  , body = forpred
                  , encode = "json")
      
      
      #http://34.73.166.192/GetAttritionPrediction1 
      
      survival <- content(res,"text")
      t1<-unlist(strsplit(survival, ","))
      t2<-as.data.frame(t1)
      d<-str_split_fixed(t2$t1, 'Probability":', 2)
      d<-as.data.frame(d)
      d<-d[!(d$V2)=="", ]
      d<-d[,2]
      d<-as.data.frame(d)
      colnames(d)<-"Probability"
      e<-str_split_fixed(t2$t1, 'Attrition":', 2)
      e<-as.data.frame(e)
      e<-e[!(e$V2)=="", ]
      e<-e[,2]
      e<-as.data.frame(e)
      colnames(e)<-"Attrition"
      
      f<-str_split_fixed(t2$t1, 'ProbableReason":', 2)
      f<-as.data.frame(f)
      f<-f[!(f$V2)=="", ]
      f<-f[,2]
      f<-as.data.frame(f)
      colnames(f)<-"ProbableReason"
      
      fff<-cbind(d,e,f)
      app3<<-cbind(fff,forpred)
      
      app3$ProbableReason<-str_replace_all(app3$ProbableReason, "[[:punct:]]", " ")
      app1<<-app3
    print("done!")
    }
    else
      
    {
      
      showNotification("Message text",
                       action = a(href = "javascript:location.reload();", "Please upload the data for prediction"))
    }
  })
  
  #Showing Survival Prediction
  output$surivalprediction<-DT::renderDataTable({
    app2},options = list(scrollX = TRUE))
  
  #Getting Survival Data
  observeEvent(input$runsurvival, {
    if(exists("forpred")){
    showTab(inputId = "tabs", target = "Survival Analysis") 
    res1 <- POST("http://34.73.166.192:80/GetSurvivalData"
                 , body = forpred
                 , encode = "json")
    survival <- content(res1,"text")
    t1<-unlist(strsplit(survival, ","))
    t2<-as.data.frame(t1)
    
    d<-str_split_fixed(t2$t1, '0.5":', 2)
    d<-as.data.frame(d)
    d<-d[!(d$V2)=="", ]
    d<-d[,2]
    d<-as.data.frame(d)
    
    e<-str_split_fixed(t2$t1, '1.0":', 2)
    e<-as.data.frame(e)
    e<-e[!(e$V2)=="", ]
    e<-e[,2]
    e<-as.data.frame(e)
    
    
    f<-str_split_fixed(t2$t1, '2.0":', 2)
    f<-as.data.frame(f)
    f<-f[!(f$V2)=="", ]
    f<-f[,2]
    f<-as.data.frame(f)
    
    fff<-cbind(d,e,f)
    colnames(fff)<-c("SixMonths","OneYear","TwoYear")
    fff$TwoYear<-str_replace_all(fff$TwoYear, "[[:punct:]]", " ")
    app2<-fff
    app2<<-cbind(app2,forpred)
    }
    else
      
    {
      
      showNotification("Message text",
                       action = a(href = "javascript:location.reload();", "Please upload the data for prediction"))
    }
  })
  
  #Updating tab
  observeEvent(input$runpred, {
    updateTabsetPanel(session, "dataset1",selected = "Attrition Prediction")
  })
  
  
  #Updating tab
  observeEvent(input$runsurvival, {
    updateTabsetPanel(session, "dataset1",selected = "Survival Analysis")
  })
  
  #About the attrition Predictor
  observeEvent(input$about, {
    showModal(modalDialog(
      title = "About the Atrrition Predictor",
      easyClose = TRUE,includeMarkdown("about.md")
    ))
  })
  
  
  #Showing instructions to upload the files
  observeEvent(input$show1, {
    showModal(modalDialog(
      title = "File Upload Instructions",
      "This is an important message!",
      easyClose = TRUE
    ))
  })
  
  output$downloadData <- downloadHandler(
    filename = function() {
      paste("download", ".csv", sep = "")
    },
    content = function(file) {
      write.csv(app1, file, row.names = FALSE)
    }
  )
  
  # Plot some general summary statistics for those who are predicted attrition.
  
  #Plotting attrition rate
  output$Plot11<-renderPlot({
    data <- df_hr1 %>% 
      group_by(Attrition) %>% 
      count() %>% 
      ungroup() %>% 
      mutate(per=`n`/sum(`n`)) %>% 
      arrange(desc(Attrition))
    data$label <- scales::percent(data$per)
    ggplot(data=data)+
      geom_bar(aes(x="", y=per, fill=Attrition), stat="identity", width = 1)+
      coord_polar("y", start=0)+
      theme_void()+
      geom_text(aes(x=1, y = cumsum(per) - per/2, label=label))+scale_fill_manual(values=c("#3399ff", "#cc3300"))
    
  })
  
  #Plotting Age with Attrition
  output$Plot12<-renderPlot({
    ggplot(df_hr1, aes(x=df_hr1$Age,fill=as.factor(Attrition) )) + geom_bar()+labs(x="Age",fill="Attrition")+scale_fill_manual(values=c("#330066", "#33cc33"))
  })
  
  
  #Plotting MonthlyIncome with Attrition
  output$Plot13<-renderPlot(
    ggplot(df_hr1, aes(MonthlyIncome))+ geom_density(aes(fill=factor(Attrition)), alpha=0.8) + 
      labs(
        x="Monthly Income",
        fill="Attrition")+scale_fill_manual(values=c("#cc3300", "#000066")
        ))
  
  
  #Plotting NumCompaniesWorked with Attrition
  output$Plot14<-renderPlot(
    ggplot(df_hr1, aes(NumCompaniesWorked)) + scale_fill_brewer(palette = "Spectral")+
      geom_histogram(aes(fill=Attrition),bins=nlevels((as.factor(df_hr1$NumCompaniesWorked))),col="black",size=.1) +
      scale_fill_manual(values=c("#56B4E9", "#E69F00"))
  )
  
  #Plotting YearsSinceLastPromotion with Attrition
  output$Plot15<-renderPlot(
    ggplot(df_hr1, aes(YearsSinceLastPromotion,fill=Attrition)) + scale_fill_brewer(palette = "Spectral")+geom_histogram( 
      bins=nlevels((as.factor(df_hr1$YearsSinceLastPromotion))), 
      col="black", 
      size=.1)+scale_fill_manual(values=c("#993333", "#009900")) 
  )
  
  #Plotting DistanceFromHome with Attrition
  output$Plot16<-renderPlot(
    ggplot(df_hr1, aes(DistanceFromHome))+ geom_density(aes(fill=factor(Attrition)), alpha=0.8) + 
      labs(
        x="Distance From Home",
        fill="Attrition")
  )
  
  #Plotting Historical data
  output$plot3 <- renderPlot({
    data()
    if (identical(input$att_vars, "Yes")) {
      df_hr %<>% filter(as.character(Attrition) == "Yes") 
    } else if (identical(input$att_vars, "No")) {
      df_hr %<>% filter(as.character(Attrition) == "No") 
    } else if (identical(input$att_vars, c("Yes", "No"))) {
      df_hr
    } else {
      df_hr <- df_hr[0, ]
    }
    
    df_hr <- filter(df_hr, JobRole %in% input$disc_vars)
    
    ggplot(df_hr, aes(JobRole, fill=Attrition)) +
      geom_bar(aes(y=(..count..)/sum(..count..)), 
               position="dodge",
               alpha=0.6) +
      scale_y_continuous(labels=percent) +
      xlab(input$disc_vars) +
      ylab("Percentage") +
      theme_bw() +
      ggtitle(paste("Count for", input$disc_vars))
  })
  
  output$plot <- renderPlot({
    data()
    if (identical(input$att_vars, "Yes")) {
      df_hr %<>% filter(as.character(Attrition) == "Yes") 
    } else if (identical(input$att_vars, "No")) {
      df_hr %<>% filter(as.character(Attrition) == "No") 
    } else if (identical(input$att_vars, c("Yes", "No"))) {
      df_hr
    } else {
      df_hr <- df_hr[0, ]
    }
    
    df_hr_final <- select(df_hr, one_of("Attrition", input$plot_vars))
    
    ggplot(df_hr_final, 
           aes_string(input$plot_vars, 
                      color="Attrition",
                      fill="Attrition")) +
      geom_density(alpha=0.2) +
      theme_bw() +
      xlab(input$plot_vars) +
      ylab("Density") +
      ggtitle(paste("Estimated density for", input$plot_vars))
  })
  
  # Monthly income, service year, etc.
  
  output$plot2 <- renderPlot({
    data()
    if (identical(input$att_vars, "Yes")) {
      df_hr %<>% filter(as.character(Attrition) == "Yes") 
    } else if (identical(input$att_vars, "No")) {
      df_hr %<>% filter(as.character(Attrition) == "No") 
    } else if (identical(input$att_vars, c("Yes", "No"))) {
      df_hr
    } else {
      df_hr <- df_hr[0, ]
    }
    
    df_hr <- filter(df_hr, 
                    YearsAtCompany >= input$years_service[1] &
                      YearsAtCompany <= input$years_service[2] &
                      JobLevel < input$job_level &
                      JobRole %in% input$job_roles)
    
    ggplot(df_hr,
           aes(x=factor(JobRole), y=MonthlyIncome, color=factor(Attrition))) +
      geom_boxplot() +
      xlab("Job Role") +
      ylab("Monthly income") +
      scale_fill_discrete(guide=guide_legend(title="Attrition")) +
      theme_bw() +
      theme(text=element_text(size=13), legend.position="top")
  })
}

#Calling application
app <- shinyApp(ui,server)
runApp(app,host="0.0.0.0",port=5050)