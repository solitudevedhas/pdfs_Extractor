#!/usr/bin/env python
# coding: utf-8


## EXTRACT CLICKY PDF DATA and STORE TO DTAFRAME

## install required Packages 
import glob ## for matching file patterns 
import os 
import re ## python regular expression
import sys 
import pandas as pd ## Data frame library
from tika import parser ## parsing the pdf files
#input_path = sys.argv[1]

###  Fetch all files in Dierctory ## 
files = glob.glob("*.pdf") ## pull all pdfs 
files_content = [] ## contents of pdf files
for i in files:
    if i.endswith(".pdf"):  # You could also add "and i.startswith('f')
        file_data = parser.from_file(i)
        all_contents = file_data['content']
        files_content.append(all_contents)


#print(files_content)    #remove "#" to print files_content
#print(len(files_content))
#print(type(files_content))

## Function for cleaning text
def clean_text(rgx_list, text):
    new_text = text
    matches = []
    for rgx_match in rgx_list:
        found_matches = re.findall(rgx_match,new_text)
        matches.append(found_matches)
        new_text = re.sub(rgx_match, '', new_text)   
    #print("No of matches Deleted :",len(matches))
    return (new_text)

### Cleaning URLs Contains in PDFs
urls = [re.compile(r'(https://.*)'),re.compile(r'(http://.*)'),re.compile(r'(\t[A-Za-z]*\s[a-z].*)')] ## pattern for match
parsed_content = []
for text in files_content:
    new_text=clean_text(urls,text)
    parsed_content.append(new_text)


## ALL VARIOUS PATERNS 
## removing values which stored alrady
all_file_names = re.compile(r'(?=ww)(.*?)(?=\n)') ## remove all file names
all_visit = re.compile(r'(?=Visits\W\s)(.*?)(?=\n)') ## remove all visits count
all_all_unique_id = re.compile(r'(?=Unique\sID\W\s)+(.*?)(?=\n)') ## remove all unique Id details
all_ip = re.compile(r'(?=IP)(.*?)(?=\n)')  ## remove all IP adress Details
all_locale = re.compile(r'(?=Locale\W\s)(.*?)(?=\n)') ## remove all Locale details
all_organization = re.compile(r'(?=Organization\W\s)(.*?)(?=\n)') ## remove all organization details
all_platforms = re.compile(r'(?=Platform\W\s)(.*?)(?=\n)|([0-9]{1,4}x[0-9]{1,4})(.*?)(?=\n)|(?=Apple\si)(.*?)(?=\n)|(?=Other)(.*?)(?=\n)') ## removing all platform details 
all_all_time_goals = re.compile(r'(?=All time goals\W\s)(.*?)(?=\n)') ## removing all time goals details 
all_dates = re.compile(r'(?=Date\W\s)(.*?)(?=\n)') ## removing visits date details 
all_landing_pages = re.compile(r'(?=Landing\spage\W\s)(.*?)(?=\n)') ## removing all landing page
all_sessions = re.compile(r'(?=Session\W\s)(.*?)(?=\n)') ## removing sessions details 
all_goals = re.compile(r'(?=Goals\W\s)(.*?)(?=\n)') ## removing goals details
all_visit_tag = re.compile(r'(Visitor\sdetail)|(This\svisit\s+First\svisit)') ## removing goals details
all_referrer = re.compile(r'(?=Referrer\W\s)(.*?)(?=\s{3,})(.*?)(?=\n)')
#all_referrer_type= re.findall(r'(?=Referrer\stype\W)\s*([A-Za-z]{1,}.)*.([A-Za-z]{1,})(?=\n)',i)
others = re.compile(r'(?=mailto\W)(.*?)(?=\n)')

All_values_matches = [all_file_names, all_visit, all_all_unique_id, all_ip, all_locale, all_organization, all_platforms, all_all_time_goals, all_dates, all_sessions, all_goals, all_visit_tag, all_landing_pages,others,all_referrer]


### Activity Patterns 
all_this_visit_activities_date = re.compile(r'([A-Z][a-z]{1,3}\s\d+\s\d+)') ## all This visit Activities Date match
all_this_visit_activity_times = re.compile(r'(\d+\W\d+\W\d+\s[ap]m)')  ## all visit Activities time details 
all_this_visit_activity_landing_pages = re.compile(r'(/.*?|\w+\W\w+/.*?|support.*?)(?=\n)')  ## all visit actiivities landing page details
#all_this_visit_activities_page_details = re.compile(r'(?=Referrer\W\s)(.*?)(?=\n)')  

 ## list of all activities matches
All_activities_matches = [all_this_visit_activities_date, all_this_visit_activity_times, all_this_visit_activity_landing_pages]# all_this_visit_activities_page_details]


## CREATE OBJECTS FOR LABLES and STORING VALUES INTO IT

visits_count = [] # count of vists 
unique_id = [] # unique id of vivitor 
Ip_address = [] # ipaddress of visitor
Locale = [] # loacality of visitor
Organization = [] # organization details
Platform = [] # platform _details 
All_time_goals = [] # al_timee_goals details
This_visit_date = [] # date of this visit
First_visit_date = [] # date of First visit
This_visit_session = [] # this visit session time 
First_visit_session = [] # first visit session time 
This_visit_referrer = [] # This visit reffer
First_visit_referrer = [] # First visit Reffer
#This_visit_referrer_type = [] # This visit Reffer_type
#First_visit_referrer_type = [] # First visit Reffer_type
This_visit_landing_page = [] # this visit landing page
First_visit_landing_page = [] # first visit landing page
This_visit_goal = [] # this time visits goal 
This_visit_activity_date = [] # This Visit Activity Date
This_visit_activity_time = [] # This Visit Activity Time
This_visit_activity_landing_page = [] # This Visit Activity landing Page
This_visit_activity_page_details = [] # This Visit Activity Page Details

for i in parsed_content: 
    visits_count_match = re.findall(r'(?<=Visits\W\s)+(.*?)(?=\n)',i)[0] # fetch visit counts
    unique_id_match = re.findall(r'(?<=Unique ID\W\s)+(.*?)(?=\n)',i)[0] # Fetch uniqe id
    Ip_address_match  = re.findall(r'(?<=IP address\W\s)+(.*?)(?=\s)',i)[0] # fetch ip_address
    Locale_match  = re.findall(r'(?<=Locale\W\s).(.*?)(?= /)',i) # locale match
    for line in Locale_match:
        Locale_match = line.replace("[","").replace("]","") # Replace Square Brackets
    Organization_match  = re.findall(r'(?<=Organization\W\s).(.*?)(?=\n)',i)[0] # organization match
    Platform_match  = re.findall(r'(?<=Platform\W\s)(.*?)(?=\n)|([0-9]{1,4}x[0-9]{1,4})(.*?)(?=\n)|(?=Apple)(.*?)(?=\n)|(?=Other)(.*?)(?=\n)',i)[0] # platform match
    All_time_goals_match  = re.findall(r'(?<=All\stime\sgoals\W\s).(.*?)(?=\n)',i) # all time goals match
    for line in All_time_goals_match:
        All_time_goals_match = line.replace("[","").replace("]","") # Replace Square Brackets
    This_visit_date_match = re.findall(r'(?<=Date\W\s)([\w{1,4}\s\w{1,4}\s]+\W\d+[ap]m)\s(.*?)(?=\n)',i)[0][0] # this visit date match
    First_visit_date_match = re.findall(r'(?<=Date\W\s)([\w{1,4}\s\w{1,4}\s]+\W\d+[ap]m)\s(.*?)(?=\n)',i)[0][1] # first visit date match
    visits_sessions_match = test=re.findall(r'(?<=Session\W\s)(\d+m\s\d+s\W\s\d+\s\w+)\s(.*?)(?=\n)',i) # visits session match
    for match in visits_sessions_match: 
        This_visit_session_match =  match[0] ## this visit session time
        First_visit_session_match = match[1] ## first visit session time 
    visits_landing_pages_match = re.findall(r'(?<=Landing page\W\s).(\W.*?)(\s.*?)(?=\n)',i) # landing page match 
    for match in visits_landing_pages_match:
        This_visit_landing_page_match = match[0] ## this visit landing page
        First_visit_landing_page_match = match[1]  ## first visit landing page 
    visit_referrer_match = re.findall(r'(?<=Referrer\W\s)(.*?)(?=\s{3,})(.*?)(?=\n)',i) ## all referrer match
    for match in visit_referrer_match:
        This_visit_referrer_match = match[0] # This visit match
        First_visit_referrer_match = match[1] # first visit match 
    #visit_referrer_type_match = 
    #for i in visit_referrer_type_match:
        #This_visit_referrer_type_match =   # This visit match pages
        #First_visit_referrer_type_match =  # first visit match pages
    This_visit_goal_match  = re.findall(r'(?<=Goals\W\s).(.*?)(?=\n)',i) # this visit goal match
    for line in This_visit_goal_match:
        This_visit_goal_match = line.replace("[","").replace("]","")
    new_clean_content = []
    new_text=clean_text(All_values_matches,i)
    new_clean_content.append(new_text)
    for n in new_clean_content:
        This_visit_activity_date_match = re.findall(r'([A-Z][a-z]{1,3}\s\d+\s\d+)',n)
        This_visit_activity_time_match = re.findall(r'(\d+\W\d+\W\d+\s[ap]m)',n)
        This_visit_activity_landing_page_match = re.findall(r'(/.*?|\w+\W\w+/.*?|support.*?)(?=\n)',n)
        #This_visit_activity_page_details_match = 
    visits_count.append(visits_count_match) ## store visits values and append list
    unique_id.append(unique_id_match) ## store unique_id values and append list
    Ip_address.append(Ip_address_match) # store visits values and append list
    Locale.append(Locale_match) ## store Ip_address values and append list
    Organization.append(Organization_match) ## store Organization values and append list
    Platform.append(Platform_match) ## store visits values and append list
    All_time_goals.append(All_time_goals_match) ## store  All time goals values and append list
    This_visit_date.append(This_visit_date_match) ## store This visit date values and append list
    First_visit_date.append(First_visit_date_match) ## store First visit date values and append list
    This_visit_session.append(This_visit_session_match) ## store This visit session values and append list
    First_visit_session.append(First_visit_session_match) ## store First visit session values and append list
    This_visit_referrer.append(This_visit_referrer_match) ## store this visit referrer match
    First_visit_referrer.append(First_visit_referrer_match) ## store First visit referrer match 
    #This_visit_referrer_type.append(This_visit_referrer_type_match) ## store this visit referrer match
    #First_visit_referrer_type.append(First_visit_referrer_type_match) ## store this visit referrer match
    This_visit_landing_page.append(This_visit_landing_page_match) ## store This visit landing page values and append list
    First_visit_landing_page.append(First_visit_landing_page_match) ## store  First visit landing page values and append list
    This_visit_goal.append(This_visit_goal_match) ## store this visit goals and appending list
    This_visit_activity_date.append(This_visit_activity_date_match)
    This_visit_activity_time.append(This_visit_activity_time_match)
    This_visit_activity_landing_page.append(This_visit_activity_landing_page_match)
    #This_visit_activity_page_details.append(This_visit_activity_page_details_match)

# create a Data frame with all values 
clicky_data = pd.DataFrame({
   "Unique ID" : unique_id, 
   "Visits" : visits_count,
   "IP address" : Ip_address,
   "Locale" : Locale,
   "Organization" : Organization,
   "Platform" : Platform,
   "All time goals" : All_time_goals,
  "This Visit Date": This_visit_date,
   "This Visit Session" : This_visit_session,
   "This Visit Referrer" : This_visit_referrer,
   "This Visit Landing Page" : This_visit_landing_page,
   "This Visit Goal" : This_visit_goal,
   "First Visit Date": First_visit_date,
   "First Visit Session" : First_visit_session,
   "First Visit Referrer" : First_visit_referrer,
   "First Visit Landing Page" : First_visit_landing_page,
   "This Visit Activity Date": This_visit_activity_date,
   "This Visit Activity Time" : This_visit_activity_time,
   "This Visit Activity Landing Page" : This_visit_activity_landing_page
   #"This Visit Activity Page Details" : This_visit_activity_page_details
})


#print(clicky_data) ## remove "#" before print for print data frame 
print(clicky_data)

## save all data to csv
#clicky_data.to_csv("clicky_data.csv")





