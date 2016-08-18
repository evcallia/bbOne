from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
# from django.core.urlresolvers import reverse
# from django.contrib import messages
# from .models import <model_name>
#CONTROLLER
#Create your views here.
def index(request):
    return render(request, 'beltOne/index.html')
