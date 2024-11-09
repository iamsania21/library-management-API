from rest_framework import serializers
from .models import Book, Borrower, Loan

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = '__all__'

from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    borrowed_date = serializers.DateField(format='%Y-%m-%d')
    return_date = serializers.DateField(format='%Y-%m-%d', required=False)

    class Meta:
        model = Loan
        fields = ['id', 'book', 'borrower', 'borrowed_date', 'return_date', 'is_returned']

