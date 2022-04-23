# COP4521GroupProject

# Problem
Our application is a textbook price tracker that scrapes websites for textbooks using Selenium. The user is given a link to the cheapest available option that was found. The user is also able to create listings to be purchased and searched for by Title or ISBN.

# Any details regarding instructions for the user interface that is beyond the obvious.
- Users must have a database schema on their machine named "pythongroup" and a user with access to that schema with a username and password (can be changed in setup.py lines 5-8 for whatever custom configurations the user wants to set). 
- In order to initialize the database, the user must run pip/pip3 install mysql.connector
- In order to initialize the web scraper, the user must run pip install selenium | By default, the webdriver requires Chrome to be installed on the machine
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
- https://www.selenium.dev/documentation/
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

- Malry Tardd: 
  - Search page for local listings and web listings
  - Selenium configuration
  - Web scraping component and compatibility
  - ISBN and Title matching
  - App routing and redirection
  - Flask configuration
  - HTML template modification
  - Login routing
  - Database management
