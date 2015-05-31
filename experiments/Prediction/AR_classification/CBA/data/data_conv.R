setwd("~/Study/Research/毕设/adm_attribution/experiments/AR_classification/CBA")
file = 'sample_4_all.csv'
data <- read.csv(file,sep=';',header=T)
data <- data[,c(-1,-2,-3,-5,-9,-17)] #drop out all zero features
y <- data$is_CVR
names(data)[c(14:23)] <- names(data)[c(15:24)]
data[,c(14:23)] <- data[,c(15:24)]
data$class <- y
data <- data[,-24]

discretize <- function(x){
    max <- max(x)
    min <- min(x)
    interval <- 1/3 * (max - min)
    breaks <- c(min - 1,interval, 2 * interval, max)
    return(cut(x,breaks=breaks,labels=c('L','M','H')))
}

data[,c(1:13)] <- apply(X=data[,c(1:13)],MARGIN=2,discretize)
write.csv(array(data[,c(1:13,24)]), file='tmp_4b.data',quote=F,row.names=F)
write.csv(array(data), file='tmp_4.data',quote=F,row.names=F)