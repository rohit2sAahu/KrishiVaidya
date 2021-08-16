from os import name
from django import http
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import redirect, render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView
from django.urls.base import reverse_lazy
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.python.keras.backend import set_session

import numpy as np
from django.urls import reverse_lazy, reverse


# main reset Form


def sign(request):
    if(request.method == "POST"):

        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']  # confirmPassword
        if(password == confirmPassword):
            if User.objects.filter(username=username).exists():
                messages.warning(request, "Name is Already Taken")
                return HttpResponseRedirect('/sign/')
            else:
                rg = User.objects.create_user(
                    username=username, email=email, password=password)
                rg.save()
                messages.success(request, "SuccessFully Account Created")
                context={'name':username}
                return render(request,'home/home.html',context)
        else:
            messages.warning(request, "PassWord Not Match")
            return HttpResponseRedirect('/sign/')
    return render(request, "home/registration.html")


def logout_up(request):
    logout(request)
    return redirect('login_up')

def login_up(request):


    if request.method == "POST":
        username = request.POST['name']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if(user is not None):
            print("get some None")
            login(request, user)
            messages.success(request, 'You are Logged in SuccessFully')
            print(request.user.username)
            name1 = request.user.username
            context = {'name': name1, 's1': "rohit"}
            return render(request, "home/home.html", context)
        else:
            messages.warning(request, 'Invalid Credentials !! ')
            return HttpResponseRedirect('/login/')

    return render(request, "home/login.html")


def prepare_image(path):


    img = load_img(path, target_size=(224, 224))
    img = img_to_array(img)
    img = img/255
    img = np.expand_dims(img, axis=0)
    return img

# return render(request, 'home/home.html')

# Create your views here.


def home(request):


    return render(request, 'home/home.html')


@login_required(login_url='login_up')
def analysis(request):


    if(request.method == 'POST'):
        file = request.FILES['imageFile']
        file_name = default_storage.save(file.name, file)
        file_url = default_storage.path(file_name)

        img = prepare_image(file_url)

        # Disease Classes
        s = {0: 'Early Blight Disease', 1: 'Healthy Plant', 2: 'Late Blight Disease', 3: 'Septorial Diseased Plant',
            4: 'Yellow Leaf Curl Virus'}

        with settings.GRAPH1.as_default():
            set_session(settings.SESS)
            predictions = settings.IMAGE_MODEL.predict(img)
            predict = np.argmax(predictions)
            predictions = s[predict]
            return render(request, "home/analysis.html", {"predictions": predictions})

    else:
        return render(request, "home/analysis.html")
    return render(request, "home/analysis.html")
def early_blight(request):
    return render(request, 'home/early_bligth.html')

def late_bligth(request):
    return render(request, 'home/late_bligth.html')

def Septorial_Disease(request):
    return render(request, 'home/Septorial_Disease.html')

def yellow_curl(request):
    return render(request, 'home/yellow_curl.html')

