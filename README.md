# Commerce

Commerce is a web-based eBay-style auction site where users can create listings, place bids, comment on items, and manage their watchlist.

![Screenshot](/auctions/static/auctions/screenshot.jpg)

## Features

- User registration and authentication

- Create and manage auction listings

- Place bids on active listings

- Add comments to listings

- Close auctions and declare winners

- Category-based listing browsing

- Watchlist functionality

## Installation Guide

### 1.) Prerequisites
Make sure you have the following installed:

• Python 3.10+ (https://www.python.org/downloads/)  
• pip (comes with Python)  
• Git (https://git-scm.com/downloads)  

### 2.) Clone the Repository
Open a terminal and run:  

`git clone https://github.com/jlzlt/Commerce.git`  
`cd Commerce`

### 3.) Install Dependencies

`pip install django`

### 4.) Run migrations

`python manage.py migrate`

### 5.) Run the server

`python manage.py runserver`

### 5.) Open in browser

Go to `http://127.0.0.1:8000/`.

## Tech Stack

• Python (Django) – Backend framework  
• JavaScript – For interactivity (optional/enhanced functionality)  
• HTML, CSS, Bootstrap – Page structure and styling  
• SQLite – Default database via Django ORM  
