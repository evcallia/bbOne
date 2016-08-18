from __future__ import unicode_literals

from django.db import models
import re
from django.contrib import messages
import bcrypt

# Create your models here.
class userManager(models.Manager):
    def process_account(self, request):
        if request.POST['type'] == 'register':
            return self.validateRegistration(request)
        else:
            return self.validateLogin(request)

    # return true if appropriate fields are valid duting registration process
    def validateRegistration(self, request):
        print 'made it'
        no_error = True
        if not self.validateEmail(request):
            no_error = False
        if not self.validateName(request):
            no_error = False
        if self.validatePassword(request) and no_error:
            User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
            return self.validateLogin(request)
        else:
            return False

    # return true if email is valid and not in use
    def validateEmail(self, request, *args):
        email = request.POST['email']
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]*$')
        if not EMAIL_REGEX.match(email):
            messages.error(request, "Email is not valid")
            return False
        else:
            # check if email is already in database
            try:
                user = User.objects.get(email=email)
                if 'edit_type' in request.POST and int(user.id) == int(args[0]):
                    return True #it's ok that the email matches, it's theirs
                else:
                    messages.error(request, "Email is already in use")
                    return False
            except User.DoesNotExist:
                pass
        return True

    def validateName(self, request):
        name = request.POST['name']
        alias = request.POST['alias']
        no_error = True
        if len(name) < 2 or any(char.isdigit() for char in name):
            messages.error(request, 'Name must be at least 2 characters and only letters')
            no_error = False
        if len(alias) < 2:
            messages.error(request, 'Alias must be at least 2 characters')
            no_error = False
        return no_error

    def validatePassword(self, request):
        password = request.POST['password']
        confirm_password = request.POST['password_confirmation']
        no_error = True
        if len(password) < 8:
            messages.error(request, 'Password must be greater than 8 characters')
            no_error = False
        if not password == confirm_password:
            messages.error(request, 'Password confirmation must match password')
            no_error = False
        return no_error

    def validateLogin(self, request):
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            if bcrypt.hashpw(password.encode(), user.password.encode()) == user.password:
                request.session['id'] = user.id
                return True
            else:
                messages.error(request, "Wrong password")
                return False
        except User.DoesNotExist:
            messages.error(request, "Invalid email")
            return False


class reviewManager(models.Manager):
    def createReview(self, request):
        if 'book_id' in request.POST:
            book = Book.objects.get(id=request.POST['book_id'])
            Review.objects.create(book=book, user=User.objects.get(id=request.session['id']), review=request.POST['review'], rating=request.POST['rating'])
            return book
        else:
            if request.POST['author_new'] == '':
                author = request.POST['author']
            else:
                author = request.POST['author_new']
            book = Book.objects.create(title=request.POST['title'], author=author)
            Review.objects.create(book=book, user=User.objects.get(id=request.session['id']), review=request.POST['review'], rating=request.POST['rating'])
            return book

class bookManager(models.Manager):
    def makeAuthors(self):
        authors = []
        for book in Book.objects.all():
            if book.author not in authors:
                authors.append(book.author)
        return authors

    def createRecents(self, id):
        # todo REVERSE THIS!!!
        recents = Review.objects.order_by('created_at').reverse()[:3]
        reviews = Review.objects.order_by('created_at').reverse()[3:]
        books = []
        for review in reviews:
            if review.book not in books:
                books.append(review.book)
        return {'recents': recents, 'books': books, 'user': User.objects.get(id=id)}


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = userManager()

#models.TextField()
#user_id = models.ForeignKey(User)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = bookManager()

class Review(models.Model):
    book = models.ForeignKey('Book')
    user = models.ForeignKey('User')
    review = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = reviewManager()





#
