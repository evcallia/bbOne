from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, Review, Book
#CONTROLLER
#Create your views here.
def index(request):
    return render(request, 'practiceBlackBelt/index.html')

def process_account(request): #:proc_login
    if User.objects.process_account(request):
        return redirect(reverse('belt:books'))
    else:
        return redirect(reverse('belt:index'))

def books(request):
    context = Book.objects.createRecents(request.session['id'])
    return render(request, 'practiceBlackBelt/books.html', context)

def books_add(request):
    authors = Book.objects.makeAuthors()
    return render(request, 'practiceBlackBelt/add.html', {'authors': authors})

def process_review(request):
    book = Review.objects.createReview(request)
    return redirect(reverse('belt:show_book', kwargs={'id': book.id}))

def delete_review(request, review_id, book_id):
    Review.objects.get(id=review_id).delete()
    return redirect(reverse('belt:show_book', kwargs={'id': book_id}))

def show_book(request, id):
    return render(request, 'practiceBlackBelt/show_book.html', {'book': Book.objects.get(id=id), 'reviews': Review.objects.all()})

def show_user(request, id):
    # pass in reviews and count reviews
    return render(request, 'practiceBlackBelt/show_user.html', {'reviews': Review.objects.filter(user=User.objects.get(id=id)), 'user': User.objects.get(id=id), 'num_reviews': Review.objects.filter(user=User.objects.get(id=id)).count()})

def logout(request):
    del request.session['id']
    return redirect(reverse('belt:index'))









#
