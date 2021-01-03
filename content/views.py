from django.shortcuts import render, HttpResponseRedirect
import numpy as np
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Cities, OurUsers, UserData
from django.utils import timezone
import sqlite3
from django.contrib.auth.decorators import user_passes_test


def index(request):
    city_list = Cities.objects.order_by('-pub_date')
    context = {
        'city_list': city_list,
    }

    return render(request, 'content/index.html', context)

   
def addcity(request):

    #Fetching data from form
    city_name = request.POST.get('city_name')
    city_description=request.POST.get('description')
    city_pub = timezone.now()


    #Correct database insert
    #city = Cities(city_name=city_name,description= city_description, pub_date = city_pub)
    #city.save()

    #Incorrect database insert
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    strinifyed_pub_date = str(city_pub)
    sql = "INSERT INTO CITIES (city_name, pub_date, description) VALUES ('"+ city_name+"','"+strinifyed_pub_date+"','"+city_description+"')"
    result = cursor.executescript(sql)
    conn.commit()
    return HttpResponseRedirect('/')
    

def userinput(request):
    return render(request, 'content/userinput.html')

def handleuserinput(request):
    #Fetching data from form
    name_in = request.POST.get('name')
    social_security_in=request.POST.get('social_security')
    my_issue_in =request.POST.get('my_issue')

    #Database input using table with no encryption of social security data  
    userdata = UserData(name=name_in,social_security = social_security_in,my_issue=my_issue_in)
    userdata.save()

    return HttpResponseRedirect('userinput')  

def check_admin(user):
   return user.is_superuser

#@user_passes_test(check_admin,login_url='/fail')   
@login_required
def machinelearning(request):
    loaded_model = np.load('finalized_model.P')
    #Here we will use the model and then we will output the result to ml.html
    return render(request, 'content/ml.html')    

def fail(request):
    return HttpResponse("The page you tried to access requires admin credentials")
