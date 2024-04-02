# Menu

A simple application based on Django and the Django Rest Framework for managing restaurant menus.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
- [API Documentation](#api-documentation)


## Features
- **Menu overview**: Unauthorised users are able to view the menus created for preview purposes.
- **Menu management**: Authorised users of the system can manage (view, create, edit, delete) menu tabs. 
- **Reporting**: Authorised users of the system are informed of menu changes once a day by email.

## Requirements

- **Python**: This application requires **Python 3.10** or later. You can download and install Python from the [official Python website](https://www.python.org/).

- **Docker** *(optional)*: Ensure that Docker is installed on your system. You can download and install Docker Desktop from the [official Docker website](https://www.docker.com/).

- **Docker Compose** *(optional)*: Docker Compose is used for orchestrating multi-container Docker applications. It should be included with Docker Desktop installation on most platforms. If not, make sure to install Docker Compose separately following the instructions provided on the [Docker Compose documentation](https://docs.docker.com/compose/install/).

## Getting Started

### Installation

1. **Clone the repository**: Clone the repository to your local machine using Git:
    ```bash
    git clone https://github.com/Dejvinczi/Menu.git
    ```

2. **Create .env**: Create an .env file from the .env.template:
    ```bash
    cp .env.template .env
    ```

4. **Set Up Environment Variables**: 
    ```bash
    # Create an .env file using this template

    # Basic Django settings
    DEBUG=True or False # True
    SECRET_KEY="your_django_secret_key" #strong-secret-key
    ALLOWED_HOSTS=your_allowed_hosts_str_splitted_with_comma # 127.0.0.1,localhost

    # Celery settings
    CELERY_BROKER_URL=your_celery_broker_url # redis://localhost:6379
    CELERY_RESULT_BACKEND=your_celery_result_backend # redis://localhost:6379

    # Sending email settings
    EMAIL_HOST=your_email_server_host # smtp.gmail.com
    EMAIL_PORT=your_email_server_port # 587
    EMAIL_USE_TLS=True or False # True
    EMAIL_HOST_USER=your_email_user@example.com # your_email@gmail.com
    EMAIL_HOST_PASSWORD=your_email_password # xxx xxxx xxxx xxxx
    DEFAULT_FROM_EMAIL=your_email_user@example.com # your_email@gmail.com

    # Database settings
    DB_ENGINE=your_db_engine # django.db.backends.postgresql
    DB_NAME=your_db_name # db_name
    DB_USER=your_db_user # db_user
    DB_PASSWORD=your_db_user_password # db_user_pass
    DB_HOST=your_db_host # 127.0.0.1
    DB_PORT=your_db_port # 5432
    ```

5. **Build Docker containers** *(Optional)*: Use Docker Compose to build the Docker containers defined in one of the composition files `docker-compose.yaml`, `docker-compose.development.yaml`, `docker-compose.production.yaml`:
    ```bash
    docker-compose -f <docker_compose_file> build
    ```

### Usage
- **Using bash script**: 
The script is divided into several stages: Depending on the DEBUG setting, it creates a development or production environment. The first step is to activate the virtual environment (if it does not exist, it will create it). The second stage is to load the environment variables. The third stage is the installation of the required packages. The 4th stage is to perform the necessary database migrations. The last (5th stage) is to start the server:
    ```bash
    ./start.sh
    ```

- **Start Docker containers**: Start the Docker containers using Docker Compose:
    ```bash
    docker-compose -f <docker_compose_file> up
    ```

## API Documentation
The API documentation is available at:<br /> 
**http://127.0.0.1:8000/api/schema/swagger-ui/**<br />
it is also possible to download the schema at:<br />
**http://127.0.0.1:8000/api/schema/**.