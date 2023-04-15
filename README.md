# Library Management System

This library management system allows users to manage libraries, books, and authors using a set of services and repositories.

## Table of Contents

- [Overview](#Overview)
- [Services](#Services)
  - [LibraryService](#LibraryService)
  - [BookService](#BookService)
  - [AuthorService](#AuthorService)
- [Repositories](#Repositories)
  - [LibraryRepository](#LibraryRepository)
  - [BookRepository](#BookRepository)
  - [AuthorRepository](#AuthorRepository)
- [Usage](#Usage)
  - [Setting Up the Database](#Setting-Up-the-Database)
  - [Adding a Library, Book, or Author](#Adding-a-Library,-Book,-or-Author)
  - [Getting Libraries, Books, or Authors](#Getting-Libraries,-Books,-or-Authors)
  - [Updating a Library, Book, or Author](#Updating-a-Library,-Book,-or-Author)
  - [Deleting a Library, Book, or Author](#Deleting-a-Library,-Book,-or-Author)

## Overview

The library management system is designed to help manage libraries, books, and authors. It consists of services and repositories to interact with the database and perform CRUD operations. The system uses FastAPI as a web framework and SQLAlchemy as an ORM.

## Services

### LibraryService

File: `app/services/library.py`

The LibraryService class contains methods to manage libraries, including getting libraries by ID or name, creating a new library, deleting a library, and updating a library.

### BookService

File: `app/services/book.py`

The `BookService` class contains methods to manage books, including getting books by ID or name, creating a new book, deleting a book, and updating a book.

### AuthorService

File: `app/services/author.py`

The `AuthorService` class contains methods to manage authors, including getting authors by ID or name, creating a new author, deleting an author, and updating an author.

## Repositories

### LibraryRepository

File: `repositories/library.py`

The `LibraryRepository` class contains methods to interact with the database for library-related operations. It supports getting libraries by ID or name, adding a library, deleting a library, and updating a library.

### BookRepository

File: `repositories/book.py`

The `BookRepository` class contains methods to interact with the database for book-related operations. It supports getting books by ID or name, adding a book, deleting a book, and updating a book.

### AuthorRepository

File: `repositories/author.py`

The `AuthorRepository` class contains methods to interact with the database for author-related operations. It supports getting authors by ID or name, adding an author, deleting an author, and updating an author.

## Usage

### Setting Up the Database

Before you can use the library management system, you need to set up the database. To do this, you'll need to create a database and configure the connection string in the application's settings.

### Adding a Library, Book, or Author

To add a new library, book, or author, you can use the `create_library`, `create_book`, or `create_author` methods in their respective services. These methods take an instance of the corresponding schema class (`LibrarySchemaIn`, `BookSchemaIn`, or `AuthorSchemaIn`) as an argument.

### Getting Libraries, Books, or Authors

To get a list of all libraries, books, or authors, you can use the `get_library`, `get_book`, or `get_author` methods in their respective services. These methods support getting records by ID or name as well.

### Updating a Library, Book, or Author

To update an existing library, book, or author, you can use the `update_library`, `update_book`, or `update_author` methods in their respective services. These methods require the ID of the record to be updated and an instance of the corresponding schema class (`LibrarySchemaIn`, `BookSchemaIn`, or `AuthorSchemaIn`) containing the updated data.

### Deleting a Library, Book, or Author

To delete a library, book, or author, you can use the `delete_library`, `delete_book`, or `delete_author` methods in their respective services. These methods require the ID of the record to be deleted.

## License

This library management system is available under the [MIT license](LICENSE).
