from django.shortcuts import render
from .models import Book
from datetime import datetime

def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all().order_by('pub_date')
    
    book_data = [
        {
            'name': book.name,
            'author': book.author,
            'pub_date': book.pub_date.strftime('%Y-%m-%d')
        }
        for book in books
    ]
    
    context = {
        'books': book_data,
        'show_pagination': False 
    }
    return render(request, template, context)

def books_date_view(request, date):
    template = 'books/books_list.html'
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return render(request, template, {'books': []})
    
    books = Book.objects.filter(pub_date=date_obj).order_by('pub_date')
    
    prev_book = Book.objects.filter(pub_date__lt=date_obj).order_by('-pub_date').first()
    next_book = Book.objects.filter(pub_date__gt=date_obj).order_by('pub_date').first()
    
    book_data = [
        {
            'name': book.name,
            'author': book.author,
            'pub_date': book.pub_date.strftime('%Y-%m-%d')
        }
        for book in books
    ]
    
    context = {
        'books': book_data,
        'show_pagination': True,
        'prev_date': prev_book.pub_date.strftime('%Y-%m-%d') if prev_book else None,
        'next_date': next_book.pub_date.strftime('%Y-%m-%d') if next_book else None,
    }
    return render(request, template, context)
