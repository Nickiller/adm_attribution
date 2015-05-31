require('caret')
setwd("~/Study/Research/毕设/adm_attribution/experiments/LR/CV/1")
calF1 <- function(table){
    TN = table[1,1]
    FN = table[1,2]
    TP = table[2,2]
    FP = table[2,1]
    accu = (TN + TP) / (TN + FN + TP + FP)
    pre = TP/(TP + FP)
    recall = TP/(TP + FN)
    F1 = (2 * pre * recall) / (pre + recall)
    cat('Accuracy:',accu,'\n')
    cat('Precision:',pre,'Recall:',recall,'F1-score:',F1,'\n')
    return(list(pre,recall,F1))
}

for(fold in 1:10){
    cat('Training for fold:', fold,'\n')
    
    train_file = paste('sample_1_train_fold_',fold,'.csv',sep='')
    test_file = paste('sample_1_test_fold_',fold,'.csv',sep='')
    train <- read.csv(file=train_file, header=T, sep=';')
    test <- read.csv(file=test_file, header=T, sep=';')
    train <- train[,2:30]
    test <- test[,2:30]
    train$is_CVR <- factor(train$is_CVR)
    test$is_CVR <- factor(test$is_CVR)
    imp.feature <- names(train)[20:29]
    cat('Imp feature list:\n',imp.feature,'\n')

    cv.imp.train <- train
    cv.base.train <- train[,1:19]
    cv.imp.test <- test
    cv.base.test <- test[,1:19]
    
    cat('Generate imp model...\n')
    cv.imp.lr <- train(cv.imp.train$is_CVR~.,data=cv.imp.train,method='svmLinear')
    cat('Generate base model...\n')
    cv.base.lr <- train(cv.base.train$is_CVR~., data=cv.base.train, method='svmLinear')

    cv.imp.pred <- predict(cv.imp.lr,cv.imp.test[,-19])
    cv.base.pred <- predict(cv.base.lr,cv.base.test[,-19])
    cv.imp.test$p_CVR <- cv.imp.pred
    cv.base.test$p_CVR <- cv.base.pred
    cv.imp.t <- table(cv.imp.pred,cv.imp.test$is_CVR)
    cv.base.t <- table(cv.base.pred,cv.base.test$is_CVR)
    cat('Result for improved lr of fold',fold,'\n')
    cv.imp.res <- calF1(cv.imp.t)
    cat('Result for base lr of fold',fold,'\n')
    cv.base.res <- calF1(cv.base.t)
    cat('===================================\n')
}
