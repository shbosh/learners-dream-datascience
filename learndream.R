
# install relevant packages
if(!require('pacman')) install.packages('pacman', repos = "http://cran.us.r-project.org")
if(!require('dplyr')) install.packages('dplyr', repos = "http://cran.us.r-project.org")
if(!require('DT')) install.packages('DT', repos = "http://cran.us.r-project.org")
if(!require('lubridate')) install.packages('lubridate', repos = "http://cran.us.r-project.org")


pacman::p_load(RMySQL, dplyr, DT, lubridate)

setwd('/Users/benjamin/desktop/learnerdream')


# Data Loading
#172
udacity = read.csv("udacity.csv", header = TRUE) 
#1423
edx = read.csv("edx.csv", header = TRUE)
#413
coursera_courses = read.csv("coursera_courses.csv", header = TRUE)
coursera_sessions = read.csv("coursera_sessions.csv", header = TRUE)
coursera_categories = read.csv("coursera_categories.csv", header = TRUE)

## Relevant Rows
# duration/3, durationunit/4, expected_learning/5, homepage/8, level/12, new_release/13, 
# required_knowledge/17, short summary/18, subtitle(title)/21, summary/22, syllabus/23, title/25, tracks/26
udacity = udacity %>% select(c(4,5,6,10,14,15,19,20,23,24,25,27,28))

# Further Data Cleaning : Number of days required, create labels for the type of course

# What data would be useful to implement a constraint-based knowledge recommender system?
# Time needed to complete the course
# Level needed (beginner/advanced)
# Required Knowledge
# Short Summary/Summary
# Syllabus --> Keyword matching 
# HomePage --> For the system to send the user to that link


# Build an algorithm that can extract keywords from a given text
