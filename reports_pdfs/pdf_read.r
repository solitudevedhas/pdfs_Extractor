# Import packages

library(rJava)
library(tabulizer)
library(tabulizerjars)
library(tidyverse)

pdf_contents <- extract_tables("Report_1600821.pdf")

## Drop First and last page
pdf_content  <- pdf_contents[-1] ## drop 1 st page
pdf_content <- pdf_content[-length(pdf_content)] ## drop last page


pdf_content_df  <-  data.frame()
for (i in pdf_content) {
    page_df <- i %>% data.frame
    page_df <- page_df[-c(1,2),]
    drops <- c("X2","X4","X6")
    page_df <- page_df[ , !(names(page_df) %in% drops)]
    pdf_content_df <- rbind(pdf_content_df,page_df)
}

colnames(pdf_content_df) <- c("Interface ID","Supplier", "Rejection Reason" , "Value")

rownames(pdf_content_df) <- NULL

test_df = pdf_content_df
