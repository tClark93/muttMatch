from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Shelter, Animal, UserManager, AnimalManager


def index(request):
    return render(request, 'game/index.html')
    
def about(request):
    return render(request, 'game/about.html')

def how(request):
    return render(request, 'game/how.html')

def login(request):
    return render(request, 'game/login.html')

def register(request):
    return render(request, 'game/register.html')

def shelter(request):
    return render(request, 'game/shelter_login.html')

def play(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        'user': user,
        'animals': Animal.objects.exclude(liked_by=user).exclude(passed_by=user)
    }
    return render(request, 'game/play.html', context)

def shelterHome(request):
    shelter = Shelter.objects.get(id=request.session['id'])
    context = {
        'shelter': shelter,
        'animals': Animal.objects.filter(location=shelter)
    }
    return render(request, 'game/shelter_home.html', context)

def registerUser(request):
    errors = User.objects.validReg(request.POST)
    if len(errors):
        for message in errors:
            messages.error(request, message)
        return redirect('/register')
    request.session['id'] = User.objects.get(email=request.POST['email']).id
    print(request.session['id'])
    return redirect('/play')

def loginUser(request):
    if User.objects.filter(email=request.POST['email']):
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['id'] = User.objects.get(email=request.POST['email']).id
            return redirect ('/play')
    messages.error(request, 'Email and Password do not match')
    return redirect('/login')

def loginShelter(request):
    if Shelter.objects.filter(id=request.POST['shelter_id']):
        shelter = Shelter.objects.get(id=request.POST['shelter_id'])
        if request.POST['password'] == shelter.password:
            request.session['id'] = shelter.id
            return redirect ('shelter/home')
    messages.error(request, 'ID and Password do not match')
    return redirect('/shelter')

def registerAnimal(request):
    errors = Animal.objects.validAnimal(request.POST)
    if len(errors):
        for message in errors:
            messages.error(request, message)
        return redirect('/shelter/home')
    return redirect('/shelter/home')

def like(request):
    user=User.objects.get(id=request.session['id'])
    animal = Animal.objects.get(id=request.POST['animal'])
    animal.liked_by.add(user)
    animal.save()
    return redirect('/play')

def dislike(request):
    print('button works')
    user=User.objects.get(id=request.session['id'])
    animal = Animal.objects.get(id=request.POST['animal'])
    animal.passed_by.add(user)
    animal.save()
    return redirect('/play')

def logout(request):
    print('logging off')
    request.session.clear()
    print(request.session)
    return redirect('/')