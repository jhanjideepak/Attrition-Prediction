
shinyServer(function(input,output,session) {
  #===============================================================================#
  #                        DASHBOARD SERVER FUNCTIONS                            #
  #===============================================================================#
  
  
  #Read the data the json data
  json_file1 <<- "http://34.73.166.192/GetDashboardData"
  df_hr1<<-fromJSON(json_file1)
  
  
  
  #Read  historical data
  filedata <-reactive({
    inFile <- input$file1
      if (is.null(inFile))
      {
      return(NULL)
      }
    df_hr<<-read.csv(inFile$datapath, header = input$header)
    return(df_hr)
  })
  
  
  
  
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
  
  
  
  #Showing historical data on the UI 
  output$hrtable1<-DT::renderDataTable({
    df_hr},options = list(scrollX = TRUE))
  
  
  
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
  
 # output$surivalprediction<-DT::renderDataTable({
 #   app2},options = list(scrollX = TRUE))
  
  observeEvent(input$showTab, {
    showTab(inputId = "tabs", target = "Analysis")
  })
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
    print("doing...")
    showTab(inputId = "tabs", target = "Attrition Prediction")
    res <- POST("http://34.73.166.192/GetAttritionPrediction"
                , body = forpred
                , encode = "json")
    appData1 <<- content(res,"text")
    h=data.frame(as.list(appData1))
    colnames(h)<-"prob"
    final=separate_rows(h,prob, convert = TRUE)
    colnames(final)<-"prob"
    
    final<<-as.data.frame(final)
    final<<-final[-1,]
    final<<-as.data.frame(final)
    final1<<-final[-nrow(final),]
    final1<<-as.data.frame(final1)
    final1<<-final[-1,]
    final1<<-as.data.frame(final1)
   
    final1<<-final1[-nrow(final1),]
    final1<<-as.data.frame(final1)
    colnames(final1)<-"Prob"
    final1$AttritionPrediction<-ifelse(final1$Prob>=0.5, "Yes", "No")
    app<<-cbind(final1,forpred)
   
    
    app1<<-app
    print("done!")
  })
  
  
  output$surivalprediction<-DT::renderDataTable({
    app2},options = list(scrollX = TRUE))
  
  #Getting Survival Data
  observeEvent(input$runsurvival, {
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
  })
  
  
  observeEvent(input$runpred, {
    updateTabsetPanel(session, "dataset1",selected = "Attrition Prediction")
  })
  
  observeEvent(input$runsurvival, {
    updateTabsetPanel(session, "dataset1",selected = "Survival Analysis")
  })
  
  
  observeEvent(input$about, {
    showModal(modalDialog(
      title = "About the Atrrition Predictor",
      easyClose = TRUE,includeMarkdown("about.md")
    ))
  })

  
  
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
})
