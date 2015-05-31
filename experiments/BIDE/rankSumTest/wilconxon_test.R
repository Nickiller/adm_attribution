setwd("~/Study/Research/毕设/adm_attribution/experiments/BIDE/rankSumTest")
data <- read.csv('pdb_rank.csv',header=F,sep='\t')
rank.one <- data$V2
rank.two <- data$V3
rank.three <- data$V4
rank.four <- data$V5
res.12 <- wilcox.test(rank.one,rank.two,paired=TRUE,conf.level=0.95,exact=T)
res.13 <- wilcox.test(rank.one,rank.three,paired=TRUE,conf.level=0.95,exact=T)
res.14 <- wilcox.test(rank.one,rank.four,paired=TRUE,conf.level=0.95,exact=T)
res.23 <- wilcox.test(rank.two,rank.three,paired=TRUE,conf.level=0.95,exact=T)
res.24 <- wilcox.test(rank.two,rank.four,paired=TRUE,conf.level=0.95,exact=T)
res.34 <- wilcox.test(rank.three,rank.four,paired=TRUE,conf.level=0.95,exact=T)