# Library Management

This library management allows users to manage libraries, books, and authors using a set of services and repositories.

## Table of Contents

- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [File Structure](#file-structure)
- [License](#license)

## Installation

1. Clone the repository

```bash
git clone https://github.com/ciastelix/library-management.git
```

2. Change the working directory to the project folder:

```bash
cd library-management
```

3. Install the dependencies using PDM:

```bash
pdm install
```

4. Create a `.env` file in the root directory of the project and add the following environment variables:

```bash
# Database
DATABASE_URL=sqllite:///db.sqlite3
```

## Running the Application

To run the application, use the following command:

```bash
pdm run uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000/`.

## API Endpoints

The following endpoints are available:

- /library: Retrieve a list of all libraries or create a new library; update, or delete a specific library by its ID
- /author: Retrieve a list of all authors or create a new author; update, or delete a specific author by its ID
- /book: Retrieve a list of all books or create a new book; update, or delete a specific book by its ID

## File Structure

- `app/`: Main application folder
  - `models.py`: SQLAlchemy models for the database
  - `schemas.py`: Pydantic schemas for data validation and serialization
  - `services/`: Service classes that handle business logic
    - `library.py`: Library service class
    - `book.py`: Book service class
    - `author.py`: Author service class
  - `repositories/`: Repository classes that handle database operations
    - `library.py`: Library repository class
    - `book.py`: Book repository class
    - `author.py`: Author repository class
    - `db_session_handler.py`: Helper functions for database session management
  - `containers.py`: Dependency injection container for the application
  - `db.py`: Database configuration and session management
- `main.py`: FastAPI application entry point
