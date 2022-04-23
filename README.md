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
- https://stripe.com/docs/api

# Extra Features
- Users are able to add listings and purchase other listings that have been posted to the database.

# Separation of work
- Madeline Marks: 
  - setup.py
  - MySQL configuration
  - Templates (.html files)
  - App routing
  - Add user function
  - Login function
  - Add listing function
  - Login attempt function
  - Appropriate Database actions for functions listed above
  - ReadME
  
- Jesus Sanchez:
  - MySQL configuration
  - Stripe configuration
  - Templates (.html files)
  - App routing
  - View listing function
  - Checkout function
  - Success function

 - Akeila Reid: 
  - setup.py
  - Templates (.html files)
  - UserExists function
  - Add User function
  - Login Attempt function
  - Hashed and stored passwords in database from addUser function
  - Login authentication in the loginAttempt function
  - App routing
