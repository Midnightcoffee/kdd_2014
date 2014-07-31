#get libraries 
library(Matrix)
library(glmnet)
# read in files
projects = read.csv("projects.csv")
outcomes = read.csv("outcomes.csv")
sampleSubmission = read.csv("sampleSubmission.csv")
#only exciting?
outcomes <- outcomes[,c(1:2)]

# inner join on projects
train <- merge(projects,outcomes,by.x="projectid",by.y="projectid")
train$date_posted <- as.Date(as.character(train$date_posted))
# only train on those past 2013
train1 <- subset(train , date_posted >= "2013-01-01")

# process is_exciting columns into 0, 1
train1$is_exciting <- as.character(train1$is_exciting)
train1$is_exciting[train1$is_exciting=="f"]<-0
train1$is_exciting[train1$is_exciting=="t"]<-1
train1$is_exciting <- as.numeric(train1$is_exciting)

#attach make attribute access easier.
attach(train1)
train1 <- train1[order(date_posted),]
print(head(train1))
train1[is.na(train1$students_reached),32] <- 32
print("----------------------------------------------")
print(head(train1))

trainy <- as.character(train1$is_exciting)
trainy[trainy=="f"] <- 0
trainy[trainy=="t"] <- 1
trainy <- as.numeric(trainy)

trainx <- train1[,-c(1:7,9,35:36)]

trainx1 <- sparse.model.matrix(~.,trainx)

test <- merge(projects,sampleSubmission,by.x="projectid",by.y="projectid")

testx <- test[,names(trainx)]

testx[is.na(testx$students_reached),24] <- 32

testx1 <- sparse.model.matrix(~.,testx)

model <- glmnet(trainx1,trainy,family="binomial",alpha=0.2,lambda=0.3602196)

pred <- predict(model,testx1,type="response")

pred <- data.frame(test$projectid,pred)
names(pred) <- names(sampleSubmission)

train1$students_reached <- as.numeric(as.character(train1$students_reached))

testx$students_reached <- as.numeric(as.character(testx$students_reached))

write.csv(pred,file="pred.csv",row.names=FALSE)


