# Event Calendar

The **Event Calendar** application is a full-stack web application built with Django that allows users to check the planned events. The application is containerized with Docker, making it easy to deploy and run in various environments.

There is also a second branch - feat/cron. It provides the celery worker which has scheduled task for requesting data from api and stores it in the db, so it can be then inspected in the future.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Tests](#tests)


## Features

- View upcoming events.
- Get the details of a certain event.
- Filter events by tags.

## Technologies

- Django
- Docker

## Requirements

- Docker
- Docker-compose

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/gzukowski/event-calendar.git
   cd event-calendar
   ```

2. Create a `.env` file based on the `.env-example` file:


3. Configure the environment variables in the `.env` file as needed.

## Running the Application

To start the application, use the Docker Compose command:

```bash
docker-compose up --build
```

The application will be available at [http://localhost:8000](http://localhost:8000).

## Usage

Once the application is running, visit the homepage where you can inspect the planned events.

## Tests
Run unit tests for views and utils. Make sure you have all modules installed !

```bash
    pip install -r requirements.txt
```

```bash
    python manage.py test events.tests
```

for linux

```bash
    python3 manage.py test events.tests
```

## Deployment
To check the steps before the deployment:

```bash
    python manage.py check --deploy
```
for linux:

```bash
    python3 manage.py check --deploy
```