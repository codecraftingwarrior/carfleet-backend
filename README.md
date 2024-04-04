# CarFleet-API

CarFleet-API is a fleet management information system designed to facilitate the management, purchase and sale of vehicles. 
This API is designed with the Django Rest Framework and is to be consumed by front-end applications, such as React or Angular, to provide a rich, interactive user interface. 
CarFleet-API integrates real-time functionalities via the use of websockets, enabling users to instantly view vehicle updates without having to refresh their browser.

## Features

- List of available vehicles, brands and manufacturer
- Buy and sell vehicles
- Real-time notifications of vehicle updates
- User authentication and authorization
- Interactive API documentation with Swagger at `/api/docs/`

## Prerequisites

Before you start, make sure you have installed :
- Python 3.8 or later
- PostgreSQL
- A Python virtual environment (recommended)

## Installation

Clone the repository and install the dependencies: :

```bash
git clone https://github.com/votreusername/carfleet-api.git
cd carfleet-api
pip install -r requirements.txt
```
## Configuration

### Configure your PostgreSQL database in the .env file :

```env
DATABASE_URL=postgres://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME
```
### Run the migrations :

```bash
python manage.py migrate
```

## Usage

### Run the development server :

```bash
python manage.py runserver
```

### To populate the database with initial data :

```bash
python manage.py populate_database
```

## Swagger API Documentation
To access the interactive API documentation, visit `/api/docs/` after launching the development server. You'll find sample requests and be able to test the API live.
