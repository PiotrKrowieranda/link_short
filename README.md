Link Shortener Application
Introduction

The Link Shortener Application is a Django-based system that allows users to shorten URLs. It provides functionality for user registration, login, link shortening, link details viewing, and redirection to the original URLs.
Features

    User Registration and Authentication: Users can register for an account and authenticate themselves to access the application.
    Link Shortening: Users can shorten long URLs to make them more manageable and shareable.
    Link Details Viewing: Users can view details of the shortened links, including the original URL and the shortened URL.
    Link Redirection: Shortened URLs redirect users to the original long URLs when accessed.
    User-Specific Links: Each user can manage their own set of shortened links.

Installation

    Clone the repository to your local machine.
    Install the required dependencies listed in the requirements.txt file using pip install -r requirements.txt.
    Run migrations using python manage.py migrate.
    Start the development server with python manage.py runserver.
