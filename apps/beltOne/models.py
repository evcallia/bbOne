from __future__ import unicode_literals

from django.db import models
import re
from django.contrib import messages
import bcrypt
from datetime import datetime


# Create your models here.

class userManager(models.Manager):
    # return true if appropriate fields are valid duting registration process
    def validateRegistration(self, request):
        no_error = self.validateName(request)
        if not self.validatePassword(request):
            no_error = False
        if no_error:
            User.objects.create(name=request.POST['name'], username=request.POST['username'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
                #this will log them in once their information has been checked
            return self.validateLogin(request)
        return False

    def validateName(self, request):
        name = request.POST['name']
        username = request.POST['username']
        no_error = True
        if len(name) < 3 or any(char.isdigit() for char in name):
            messages.error(request, 'Frist name must be 3 characters and only letters')
            no_error = False
        if len(username) < 3:
            messages.error(request, 'Last name must be 3 characters and only letters')
            no_error = False
        try:
            User.objects.get(username=username)
            messages.error(request, 'Username is already taken')
            no_error = False
        except:
            pass
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
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            if bcrypt.hashpw(password.encode(), user.password.encode()) == user.password:
                request.session['id'] = user.id
                return True
            messages.error(request, "Invalid password")
        except User.DoesNotExist:
            messages.error(request, "Invalid username")
            return False



class tripManager(models.Manager):
    def add(self, request):
        if self.validateInfo(request) and self.validateDates(request):
            Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], planned_by=User.objects.get(id=request.session['id']))
            return True
        else:
            return False

    def validateInfo(self, request):
        no_error = True
        if request.POST['destination'] == '':
            messages.error(request, 'Destination cannot be blank')
        if request.POST['description'] == '':
            messages.error(request, 'Description cannot be blank')
            no_error = False
        return no_error

    def validateDates(self, request):
        no_error = True
        if request.POST['start_date'] == '':
            messages.error(request, 'Travel date from cannot be blank')
            no_error = False

        if request.POST['end_date'] == '':
            messages.error(request, 'Travel date to cannot be blank')
            no_error = False
        date_format = "%Y-%m-%d"
        if no_error:
            start = datetime.strptime(request.POST['start_date'], date_format)
            end = datetime.strptime(request.POST['end_date'], date_format)
            now = datetime.now()
            if start < now:
                messages.error(request, 'Start date cannot be in the past')
                no_error = False
            if end < start:
                messages.error(request, 'End date cannot be before start')
                no_error = False
        return no_error

    def join(self, request, id):
        context = self.getTrips(request)
        my_trip = Trip.objects.get(id=id)
        can_join = True
        for trip in context['joined_trips']:
            if my_trip == trip.trip:
                can_join = False
        if can_join:
            User_Trip.objects.create(user=User.objects.get(id=request.session['id']), trip=Trip.objects.get(id=id))
        else:
            messages.error(request, "You've already joined this trip!")

    def getTrips(self, request):
        user = User.objects.get(id=request.session['id'])
        try:
            joined_trips = User_Trip.objects.filter(user=user)
        except:
            joined_trips = []

        other_trips = Trip.objects.all().exclude(planned_by=user)


        context = {
        'user': user,
        'user_trips': Trip.objects.filter(planned_by=user),
        'joined_trips': joined_trips,
        'other_trips': other_trips,
        # 'other_joined_trips':
        }
        return context


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_date = models.DateField(max_length=50)
    end_date = models.DateField(max_length=50)
    planned_by = models.ForeignKey('User')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = tripManager()

class User_Trip(models.Model):
    user = models.ForeignKey('User')
    trip = models.ForeignKey('Trip')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# models.TextField()





#
