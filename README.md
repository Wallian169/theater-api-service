# Theatre-API-Service

API service for theatre management written in Django Rest Framework (DRF).

## Table of Contents

1. [Installation](#installation)
2. [Getting access](#Getting-access)
3. [Features](#features)
4. [DB Scheme](#DB-scheme)

## Installation

Make sure you have Python and Docker installed. Follow these steps to set up the project:

```bash
# Clone the repository
git clone https://github.com/Wallian169/theater-api-service.git

# Change directory into the project
cd theatre-api-service

# Set up a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install required packages
pip install -r requirements.txt

# Run migrations
python manage.py migrate    

# Start the development server
python manage.py runserver

# (Optional) Build and run with Docker
docker build .
docker-compose up
```

## Getting Access

To access the API, follow these steps:

- **Create a user account** to gain access via user/register/.
- **Authenticate** using your credentials.
- **Access the endpoints** as listed in the documentation.

## Features

1. Admin panel.
2. Creating user via email.
3. Managing own profile.
4. For Admin user added possibility to manage Plays, Performances, Theatre Halls and more.
5. Filtering Plays by name, genres and actors.
6. Creating reservation for chosen Performance.
7. Added different permissions for different actions.
8. Added tests for different endpoints.
9. JWT authenticated.
10. Documentation located at /api/doc/swagger/
11. Uploading poster to each Performance via separate endpoint


## DB Scheme

![TheatreAPI](https://github.com/Wallian169/images/blob/main/TheaterAPI_DB_sheme.jpg?raw=true)


