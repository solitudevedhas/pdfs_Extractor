#!/usr/bin/env python
# coding: utf-8


## import packages

from tabula import read_pdf
from tabulate import tabulate
import pandas as pd
import numpy



# read pdf Contents 
pdf_contents = read_pdf("Report_1600821.pdf", pages="all", multiple_tables=True)


## Drop  1st and last page in pdf contents 
pdf_content = pdf_contents
pdf_content.pop(0)
pdf_content.pop(60)


# storing all data to new pandas DataFrame
report_df = pd.DataFrame()
for i in range(len(pdf_content)):
    page = pdf_content[i]
    page = page.drop(page.index[:2]) ## Drop header of each page
    page = page.drop([1,3,5], axis=1) ## unnessary column of each page
    report_df = pd.concat([report_df, page]).replace(r'\r',' ', regex=True) ## removing white space
    
##########   
report_df = report_df.reset_index(level=None, drop=True) # reset index values


## giving header name 
report_df = report_df.rename(columns={0:'Interface ID',2 : 'Supplier', 4 : 'Rejection Reason' , 6 : 'Value'})


# Index identifier for nan values
nan_index=[]
for i,a in zip(report_df.index.values,report_df["Interface ID"].isnull()):
    if a == True:
        nan_index.append(i) 


## concate column values splited into multiple rows 
for i in nan_index:
    report_df["Supplier"][i-1] = report_df["Supplier"][i-1]+' '+report_df["Supplier"][i]
    if type(report_df["Value"][i])==float:
        report_df["Value"][i] = ""
    report_df["Value"][i-1] = report_df["Value"][i-1]+' '+report_df["Value"][i]
    

## reset index values
report_df = report_df.dropna().reset_index(level=None, drop=True)

# storing to csv
report_df.to_csv("Report_1600821.csv")

