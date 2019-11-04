## install required Packages 
import glob ## for matching file patterns 
import os 
import re ## python regular expression
import sys 
import pandas as pd ## Data frame library
from tika import parser ## parsing the pdf files
#input_path = sys.argv[1]

###########################################################################################################################

###  Fetch all files in Dierctory ## 
files = glob.glob("*.pdf") ## pull all pdfs 
files_content = [] ## contents of pdf files
for i in files:
    if i.endswith(".pdf"):  # You could also add "and i.startswith('f')
        file_data = parser.from_file(i)
        all_contents = file_data['content']
        files_content.append(all_contents)

# print(files_content)    #remove "#" to print files_content

#print(len(files_content))
#print(type(files_content))

###########################################################################################################################

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

############################################################################################################################

## removing All un nessary URLs and tab spaces 
urls = [re.compile(r'(https://.*)'),re.compile(r'(http://.*)'),re.compile(r'(\t[A-Za-z]*\s[a-z].*)')] ## pattern for match
parsed_content = []
for text in files_content:
    new_text=clean_text(urls,text)
    parsed_content.append(new_text)

############################################################################################################################

## extract variabes value
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
This_visit_landing_page = [] # this visit landing page
First_visit_landing_page = [] # first visit landing page
This_visit_goal = [] # this time visits goal 

for i in parsed_content:
    visits_count_match = re.findall(r'(?<=Visits\W\s)+(.*?)(?=\n)',i) # fetch visit counts
    unique_id_match = re.findall(r'(?<=Unique ID\W\s)+(.*?)(?=\n)',i) # Fetch uniqe id
    Ip_address_match  = re.findall(r'(?<=IP address\W\s)+(.*?)(?=\s)',i) # fetch ip_address
    Locale_match  = re.findall(r'(?<=Locale\W\s).(.*?)(?= /)',i) # locale match
    Organization_match  = re.findall(r'(?<=Organization\W\s).(.*?)(?=\n)',i) # organization match
    Platform_match  = re.findall(r'(?<=Platform\W\s).(.*?)(?=\n)',i) # platform match
    All_time_goals_match  = re.findall(r'(?<=All time goals\W\s).(.*?)(?=\n)',i) # all time goals match
    This_visit_date_match = re.findall(r'(?<=Date\W\s)([\w{1,4}\s\w{1,4}\s]+\W\d+[ap]m)\s(.*?)(?=\n)',i)[0][0] # this visit date match
    First_visit_date_match = re.findall(r'(?<=Date\W\s)([\w{1,4}\s\w{1,4}\s]+\W\d+[ap]m)\s(.*?)(?=\n)',i)[0][1] # first visit date match
    visits_sessions_match = test=re.findall(r'(?<=Session\W\s)(\d+m\s\d+s\W\s\d+\s\w+)\s(.*?)(?=\n)',i) # visits session match
    for match in visits_sessions_match: 
        This_visit_session_match =  match[0] ## this visit session time
        First_visit_session_match = match[1] ## first visit session time 
    visits_landing_pages_match = re.findall(r'(?<=Landing page\W\s).(\W.*?).(\s.*?)(?=\n)',i) # landing page match 
    for match in visits_landing_pages_match:
        This_visit_landing_page_match = match[0] ## this visit landing page
        First_visit_landing_page_match = match[1] ## first visit landing page
    This_visit_goal_match  = re.findall(r'(?<=Goals\W\s).(.*?)(?=\n)',i) # this visit goal match
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
    This_visit_landing_page.append(This_visit_landing_page_match) ## store This visit landing page values and append list
    First_visit_landing_page.append(First_visit_landing_page_match) ## store  First visit landing page values and append list
    This_visit_goal.append(This_visit_goal_match) ## store this visit goals and appending list

############################################################################################################################

#  create a Data frame with all values 
trasers_clicky_data = pd.DataFrame({
    "Unique ID" : unique_id, 
    "Visits" : visits_count,
    "IP address" : Ip_address,
    "Locale" : Locale,
    "Organization" : Organization,
    "Platform" : Platform,
    "All time goals" : All_time_goals,
    "This Visit Date": This_visit_date,
    "This Visit Session" : This_visit_session,
    "This Visit Landing Page" : This_visit_landing_page,
    "First Visit Date": First_visit_date,
    "First Visit Session" : First_visit_session,
    "First Visit Landing Page" : First_visit_landing_page
})

# print(trasers_clicky_data) ## remove "#" fore print of trasers_clicky_data
############################################################################################################################

## removeinf square Brackets "[]" from eache values in Data frame 

for i in trasers_clicky_data:
    # Removing square brackets "[]"
    trasers_clicky_data[i] = pd.DataFrame([str(line).replace("[","").replace("]","") for line in trasers_clicky_data[i]])
    # Removing small Brackets = "()"
    trasers_clicky_data[i] = pd.DataFrame([str(line).replace("'","").replace("'","") for line in trasers_clicky_data[i]])

#print(trasers_clicky_data) ## remove "#" before print for print data frame 

############################################################################################################################

## save all data to csv
trasers_clicky_data.to_csv("trasers_clicky_data.csv")

print("Done")

############################################################################################################################