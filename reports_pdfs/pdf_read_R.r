# Import Required Libraries
library(rJava)
library(tabulizer)
library(tabulizerjars)
library(tidyverse)

# Read Pdf
pdf_contents <- extract_tables("Report_1600821.pdf")

## Drop unnessary Pages
pdf_contents <- pdf_contents[-1] ## drop 1 st page
pdf_contents <- pdf_contents[-length(pdf_contents)] ## drop last page

# Creating A sigle data frame by append Data from each page called pdf_contents_DF
pdf_contents_DF  <-  data.frame() # blanck Data Frame
for (i in pdf_contents) {
    page_df <- i %>% data.frame 
    page_df <- page_df[-c(1,2),] # drop headers 
    drops <- c("X2","X4","X6")   # columns names to be Drop
    page_df <- page_df[ , !(names(page_df) %in% drops)] # drop unnessary Columns
    pdf_contents_DF <- rbind(pdf_contents_DF,page_df)
}

# columns names from Data frame
colnames(pdf_contents_DF) <- c("Interface ID","Supplier", "Rejection Reason" , "Value") 

## remove white space  from Column name Supplier and Value
pdf_contents_DF$Supplier = gsub(replacement = ' ',pattern = '\r',x = pdf_contents_DF$Supplier) 
pdf_contents_DF$Value = gsub(replacement = ' ',pattern = '\r',x = pdf_contents_DF$Value)

# Index of Nun values
nan_index=which(pdf_contents_DF$`Interface ID`=="")

#  join blank valus with their previes Index
for( i in nan_index){
    pdf_contents_DF[i-1,2] <- paste(cbind(pdf_contents_DF[i-1,2],pdf_contents_DF[i,2]), collapse=" ")
    pdf_contents_DF[i-1,4] <- paste(cbind(pdf_contents_DF[i-1,4],pdf_contents_DF[i,4]), collapse=" ")
}

# Drop all rows , Having 'NULL' Interface ID By create A subset and replace it
pdf_contents_DF = subset(pdf_contents_DF,`Rejection Reason`!="")

## write data to Csv
write.csv(pdf_contents_DF,"Report_1600821_R.csv", row.names = FALSE, quote = FALSE)

Print(" File Extration Completed ")
