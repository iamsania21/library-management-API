
# Library Management System API

This project implements a RESTful API for a library management system using Django and Django REST Framework (DRF). It allows managing books, borrowers, and loans. Users can borrow and return books, and get information on active loans and borrowing history.

## Project Overview

The Library Management System includes the following functionality:

- **Books**: Add new books to the system and list books with filter options for availability.
- **Borrowers**: Register borrowers who can borrow books.
- **Loans**: Track borrowed books and manage borrowing and returning books.

## Features

- Add new books to the library.
- Borrow books (with a borrowing limit of 3 active books).
- Return books and track their status.
- Get active loans for a borrower.
- Get the borrowing history of a borrower.

## Setup Instructions

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- pip (Python package installer)
- Django
- Django REST Framework

### Steps to Run the Project

1. **Clone the repository**  
   Clone the project from GitHub:

   ```bash
   git clone https://github.com/yourusername/library-management-system.git
   cd library-management-system
   ```

2. **Create a Virtual Environment**  
   It's recommended to use a virtual environment to manage project dependencies. You can create and activate a virtual environment like this:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**  
   Install all the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**  
   Run Django migrations to set up the database:

   ```bash
   python manage.py migrate
   ```

5. **Create Superuser (Optional)**  
   To access the Django admin panel, you can create a superuser account:

   ```bash
   python manage.py createsuperuser
   ```

   Follow the prompts to set up the superuser credentials.

6. **Run the Development Server**  
   Start the Django development server:

   ```bash
   python manage.py runserver
   ```

   Your application will be accessible at `http://127.0.0.1:8000/`.

## API Endpoints

### Book Management

- **POST /api/books/**  
  Add a new book to the library.

  **Request Body Example:**

  ```json
  {
    "title": "Book Title",
    "author": "Author Name",
    "published_date": "2024-11-09",
    "isbn": "1234567890123",
    "available": true
  }
  ```

- **GET /api/books/list/**  
  List all books. You can filter by availability using the `available` query parameter.

  **Example Request:**

  ```
  GET /api/books/list/?available=true
  ```

  **Response Example:**

  ```json
  [
    {
      "id": 1,
      "title": "Book Title",
      "author": "Author Name",
      "published_date": "2024-11-09",
      "isbn": "1234567890123",
      "available": true
    }
  ]
  ```

### Borrowing and Returning

- **POST /api/borrow/**  
  Borrow a book using `book_id` and `borrower_id`. The book’s availability will be updated, and the borrow count will be incremented.

  **Request Body Example:**

  ```json
  {
    "book_id": 1,
    "borrower_id": 1
  }
  ```

- **POST /api/return/**  
  Return a borrowed book using `book_id`. The book's availability will be updated, and the loan will be marked as returned.

  **Request Body Example:**

  ```json
  {
    "book_id": 1
  }
  ```

### Borrowed Books and Borrower History

- **GET /api/borrowed/{borrower_id}/**  
  List all active (unreturned) books for a borrower.

  **Example Request:**

  ```
  GET /api/borrowed/1/
  ```

  **Response Example:**

  ```json
  [
    {
      "id": 1,
      "book": {
        "id": 1,
        "title": "Book Title"
      },
      "borrowed_date": "2024-11-09",
      "is_returned": false
    }
  ]
  ```

- **GET /api/history/{borrower_id}/**  
  List all books ever borrowed by the borrower, including return status.

  **Example Request:**

  ```
  GET /api/history/1/
  ```

  **Response Example:**

  ```json
  [
    {
      "id": 1,
      "book": {
        "id": 1,
        "title": "Book Title"
      },
      "borrowed_date": "2024-11-09",
      "return_date": "2024-11-10",
      "is_returned": true
    }
  ]
  ```

## Error Handling

- **400 Bad Request**: If the request data is invalid.
- **404 Not Found**: If the resource is not found (e.g., borrower or book does not exist).
- **500 Internal Server Error**: If there's an unexpected server error.

## Documentation

This API follows REST principles, and all endpoints are designed to be simple and easy to use with clear error messages. The response data is returned in JSON format. For more detailed documentation on how to use the API, you can refer to the [Django REST Framework documentation](https://www.django-rest-framework.org/).

## Additional Information

- **Django Version**: 3.2+
- **Django REST Framework Version**: 3.12+
- **Database**: SQLite (by default), but you can change the database settings in `settings.py`.

