from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
# Create your views here.

#def home(request):
    #return HttpResponse("<h1>HELLO  WORLD!</h1>")

def home(request):
    return render(request, 'content.html')


def next(request):
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['pwd']
        user = User.objects.create_user(name, email, password)
        user.last_name = request.POST['lname']
        user.save()
        return render(request,'next.html',{'name':name})