from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone
from .models import Book, Borrower, Loan
from .serializers import BookSerializer, BorrowerSerializer, LoanSerializer
from django.db.models import Count

@api_view(['POST'])
def add_book(request):
    """Endpoint to add a new book."""
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_books(request):
    """Endpoint to list books, optionally filter by availability."""
    available = request.query_params.get('available')
    if available:
        books = Book.objects.filter(available=(available.lower() == 'true'))
    else:
        books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def borrow_book(request):
    """Endpoint to borrow a book if it's available and borrower's status is active."""
    book_id = request.data.get('book_id')
    borrower_id = request.data.get('borrower_id')

    try:
        book = Book.objects.get(id=book_id)
        borrower = Borrower.objects.get(id=borrower_id)

        if not borrower.is_active:
            return Response({'error': 'Borrower is inactive.'}, status=status.HTTP_403_FORBIDDEN)

        active_loans_count = Loan.objects.filter(borrower=borrower, is_returned=False).count()
        if active_loans_count >= 3:
            return Response({'error': 'Borrowing limit reached.'}, status=status.HTTP_403_FORBIDDEN)

        if not book.available:
            return Response({'error': 'Book is unavailable.'}, status=status.HTTP_400_BAD_REQUEST)

        loan = Loan.objects.create(book=book, borrower=borrower)
        book.available = False
        book.borrow_count += 1
        book.save()

        serializer = LoanSerializer(loan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except (Book.DoesNotExist, Borrower.DoesNotExist):
        return Response({'error': 'Invalid book or borrower ID.'}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Loan
from .serializers import LoanSerializer
from datetime import date

@api_view(['POST'])
def return_book(request):
    """Endpoint to return a borrowed book and update its availability."""
    book_id = request.data.get("book_id")
    try:
        # Retrieve the loan based on the book_id and ensure it's not already returned
        loan = Loan.objects.get(book_id=book_id, is_returned=False)
        
        # Mark the loan as returned
        loan.is_returned = True
        loan.return_date = date.today()  # Set the return date to today's date
        loan.save()

        # Update the book's availability
        book = loan.book
        book.available = True  # Mark the book as available
        book.save()

        # Serialize and return the loan information as response
        serializer = LoanSerializer(loan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Loan.DoesNotExist:
        # If no active loan exists for the given book_id, return an error
        return Response({"error": "Loan record not found or book already returned."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def active_loans(request, borrower_id):
    """Endpoint to list all active (unreturned) loans for a borrower."""
    loans = Loan.objects.filter(borrower_id=borrower_id, is_returned=False)
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def borrowing_history(request, borrower_id):
    """Endpoint to list all loan history for a borrower."""
    loans = Loan.objects.filter(borrower_id=borrower_id)
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)