from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, Trip, User_Trip
#CONTROLLER
#Create your views here.
def main(request):
    return render(request, 'beltOne/login.html')

def proc_login(request):
    if request.POST['type'] == 'register':
        success = User.objects.validateRegistration(request)
    else:
        success = User.objects.validateLogin(request)
    if success:
        return redirect(reverse('belt:travels'))
    else:
        return redirect(reverse('belt:main'))


def travels(request):
    context = Trip.objects.getTrips(request)
    return render(request, 'beltOne/index.html', context)

def add(request):
    if request.method == 'POST':
        #process add
        if Trip.objects.add(request):
            return(redirect(reverse('belt:travels')))
    return render(request, 'beltOne/add.html')

def join(request, id):
    Trip.objects.join(request, id)
    return redirect(reverse('belt:travels'))

def show(request, id):
    trip = Trip.objects.get(id=id)
    return render(request, 'beltOne/show.html', {'trip': trip, 'joining': User_Trip.objects.filter(trip=trip)})

def logout(request):
    del request.session['id']
    return redirect(reverse('belt:main'))








 #
