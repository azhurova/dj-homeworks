from django.shortcuts import render, redirect

from books.models import Book


def index(request):
    return redirect('books')


def books_view(request):
    books = Book.objects.all()

    template = 'books/books_list.html'
    context = {
        'books': books
    }
    return render(request, template, context)


def books_pub_date_view(request, pub_date):
    books = Book.objects.all().filter(pub_date=pub_date)

    prev_pub_date = Book.objects.all().filter(pub_date__lt=pub_date).order_by('-pub_date').values('pub_date').first()
    if prev_pub_date:
        previous_date = prev_pub_date['pub_date']
    else:
        previous_date = None

    next_pub_date = Book.objects.all().filter(pub_date__gt=pub_date).order_by('pub_date').values('pub_date').first()
    if next_pub_date:
        next_date = next_pub_date['pub_date']
    else:
        next_date = None

    template = 'books/books_list.html'
    context = {
        'books': books,
        'previous_date': previous_date,
        'next_date': next_date
    }
    return render(request, template, context)
