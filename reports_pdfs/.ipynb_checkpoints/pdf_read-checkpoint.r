# Import packages

library(rJava)
library(tabulizer)
library(tabulizerjars)
library(tidyverse)

pdf_contents <- extract_tables("Report_1600821.pdf")

pdf_content  <- pdf_contents[-1] ## drop 1 st page
pdf_content <- pdf_content[-length(pdf_content)] ## drop last page

new_pdf_content  <-  data.frame()
for (i in pdf_content) {
    page_df <- i %>% data.frame
    page_df <- page_df[-c(1,2),]
    drops <- c("X2","X4","X6")
    page_df <- page_df[ , !(names(page_df) %in% drops)]
    new_pdf_content <- rbind(new_pdf_content,page_df)
}

colnames(new_pdf_content) <- c("Interface ID","Supplier", "Rejection Reason" , "Value")

rownames(new_pdf_content) <- NULL

test_df = new_pdf_content

nan_index=list()
for (i in row.names.data.frame(test_pdf)) {
    for (a in test_df["Interface ID"]){
        print(a)
    }
    }
  
 
for (a in test_df["Interface ID"]){print(a)}
    