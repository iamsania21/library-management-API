from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.add_book, name='add_book'),
    path('books/list/', views.list_books, name='list_books'),
    path('borrow/', views.borrow_book, name='borrow_book'),
    path('return/', views.return_book, name='return_book'),
    path('borrowed/<int:borrower_id>/', views.active_loans, name='active_loans'),
    path('history/<int:borrower_id>/', views.borrowing_history, name='borrowing_history'),
    path('api/return/', views.return_book, name='return_book'),
]
