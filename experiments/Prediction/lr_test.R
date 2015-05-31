file = 'lr_1.csv'
setwd("~/Study/Research/毕设/adm_attribution/experiments")
data <- read.csv(file=file,header=T)[2:20]

require('caret')
fitControl = trainControl(method = "cv",number = 10,repeats = 30,savePredictions=T)
base.lr.fit <- train(data$is_CVR~.,data=data,method='glm',family=binomial,trControl=fitControl)
fitpred <- base.lr.fit$finalModel$fitted.values
fitpredt <- function(t) ifelse(fitpred > t , 1,0)
base.res <- confusionMatrix(fitpredt(0.5),data$is_CVR)
print(base.res$overall)