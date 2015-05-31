file = 'sample_4_all.csv'
setwd("~/Study/Research/毕设/adm_attribution/experiments/LR/CV/")
data <- read.csv(file=file,header=T,sep=';')[2:30]
base.data <- data[1:19]

data$is_CVR <- factor(data$is_CVR)
base.data$is_CVR <- factor(base.data$is_CVR)

calF1 <- function(table){
    TN = table[1,1]
    FN = table[1,2]
    TP = table[2,2]
    FP = table[2,1]
    pre = TP/(TP + FP)
    recall = TP/(TP + FN)
    F1 = (2 * pre * recall) / (pre + recall)
    cat('Precision:',pre,'Recall:',recall,'F1-score:',F1)
    return(list(pre,recall,F1))
}

# LR with 10-fold cross validation on all sample data

require('caret')
fitControl = trainControl(method = "cv",number = 10,repeats = 30,savePredictions=T)
base.lr.fit <- train(base.data$is_CVR~.,data=base.data,method='glm',family=binomial,trControl=fitControl)
imp.lr.fit <- train(data$is_CVR~.,data=data,method='glm',family=binomial,trControl=fitControl)
base.pred <- base.lr.fit$finalModel$fitted.values
imp.pred <- imp.lr.fit$finalModel$fitted.values
fitpredt <- function(t,pred) ifelse(pred > t , 1,0)
base.res <- confusionMatrix(fitpredt(0.5,base.pred),base.data$is_CVR)
imp.res <- confusionMatrix(fitpredt(0.5,imp.pred),data$is_CVR)
print(base.res$overall) # about 79.67%
print(imp.res$overall)  # about 81.90%
base.res.list <- calF1(base.res$table) # 90.96%,65.88%,76.41%
imp.res.list <- calF1(imp.res$table)   # 92.25%,69.64%,79.36%
print(base.res$table)
print(imp.res$table)
