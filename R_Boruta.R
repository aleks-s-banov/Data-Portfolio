setwd('C:\\Users\\Asus\\Documents\\Lumos project\\Rcode')
data<-read.csv('out.csv', sep=',')
str(data)
head(data)
summary(data)

# Load Packages and prepare dataset
library(caret)
library(Boruta)
data<-data[,-1]
data <- subset(data, select = -c(G1,G2))
contain <- vector(mode = "list", length = 300)


for (i in 1:10){
# Perform Boruta search
boruta_output <- Boruta(G3 ~ ., data=na.omit(data), doTrace=0)
names(boruta_output)

# Get significant variables including tentatives
boruta_signif <- getSelectedAttributes(boruta_output, withTentative = TRUE)
print(list(boruta_signif))

# Plot variable importance
plot(boruta_output, cex.axis=.7, las=2, xlab="", main="Variable Importance")  
}

