# COP4521GroupProject

# Problem
Our application is a textbook price tracker that scrapes websites for used and new textbooks using Selenium. The user is given a link to the cheapest available option that was found.

# Any details regarding instructions for the user interface that is beyond the obvious.
- Users must have a database schema on their machine named "pythongroup" and a user with access to that schema with a username and password (can be changed in setup.py lines 5-8 for whatever custom configurations the user wants to set). 
- In order to initialize the database, the user must run pip/pip3 install mysql.connector
** Put Selenium Requirements here**
** Put Stripe Requirements including .env here**

# Libraries Used
- Flask
- Selenium 
- werkzeug
- os
- mysql.connector
- sys
- time
- stripe

# Other Resources
- **Cite Selenium Here**
- **Cite Stripe Here**

# Extra Features
- Users are able to add listings and purchase other listings that have been posted to the database.

# Separation of work
- Madeline Marks: setup.py, MySQL configuration, templates (.html files), app routing, add user function, login function, add listing function, login attempt function, ReadME
