from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
# import PIL as pillow
# from PIL import Image

EMAIL_REGEX = re.compile('^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4})$')

class UserManager(models.Manager):
    def validReg(self, postData):
        errors = []
        if not postData['first_name'].isalpha():
            errors.append('Name can only contain alphabetical characters!')
        if len(postData['first_name']) < 3:
            errors.append('Name must be at least three letters!')
        if not postData['last_name'].isalpha():
            errors.append('Name can only contain alphabetical characters!')
        if len(postData['last_name']) < 3:
            errors.append('Name must be at least three letters!')
        if not re.match(EMAIL_REGEX, postData['email']):
            errors.append('Email is not valid.')
        if User.objects.filter(email=postData['email']).exists():
            errors.append('Email already exists!')
        if len(postData['zip']) != 5:
            errors.append('Zipcode must be five digits')
        if len(postData['password']) < 8:
            errors.append('Password must contain at least 8 characters!')
        if postData['password'] != postData['confirm']:
            errors.append('Passwords must match!')
        
        if not errors:
            tempPass = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            User.objects.create(first_name=postData['first_name'],last_name=postData['last_name'], email=postData['email'], zipcode=postData['zip'], password=tempPass)
            user=User.objects.get(email=postData['email'])
        return errors

class AnimalManager(models.Manager):
    def validAnimal(self, postData):
        errors = []
        if not postData['name'].isalpha():
            errors.append('Name can only contain alphabetical characters!')
        if len(postData['name']) < 2:
            errors.append('Name must be at least two letters!')
        if len(postData['descrip']) < 1:
            errors.append('Please provide a description of the animal')
        if len(postData['descrip']) > 500:
            errors.append('Description is limited to 500 characters')
        if not postData['species']:
            errors.append('Please provide species information')
        if not postData['species']:
            errors.append('Please provide breed information, if unknown, type Mixed')
        if not postData['age']:
            errors.append('Please provide age information')

        if not errors:
            Animal.objects.create(name=postData['name'],age=postData['age'], description=postData['descrip'], species=postData['species'], breed=postData['breed'], gender=postData['gender'], location=Shelter.objects.get(id=postData['shelter_id']))
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    zipcode = models.IntegerField()
    password = models.CharField(max_length=255)
    is_admin = models.CharField(max_length=200, default='User')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Shelter(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    zipcode = models.IntegerField()
    password = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Animal(models.Model):
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    species = models.CharField(max_length=255)
    breed = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=255, blank=True)
    # image = models.ImageField(upload_to='animal_image', blank=True)
    liked_by = models.ManyToManyField(User, related_name='liked', blank=True)
    passed_by = models.ManyToManyField(User, related_name='passed', blank=True)
    playdate = models.ManyToManyField(User, related_name='scheduled_playdate', blank=True)
    location = models.ForeignKey(Shelter, related_name='housing')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AnimalManager()

