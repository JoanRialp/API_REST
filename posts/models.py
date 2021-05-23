from django.db import models
from django.db.models.fields.related import create_many_to_many_intermediary_model
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your models here.

class Posts(models.Model):
    title = models.CharField(max_length=140)
    description = models.TextField()

    def __str__(self):
        return self.title + ' : ' + self.description

class Publicaciones(models.Model):
    id_user = models.IntegerField()
    name_user = models.CharField(max_length=140, default='')
    description = models.TextField()

    def __str__(self):
        return str(self.id_user) + ' : ' + self.name_user + ' : ' + self.description

class Following(models.Model):
    id_user = models.IntegerField()
    id_UserFlollowing = models.IntegerField()

    def __str__ (self):
        return str(self.id_user) + ' : ' + str(self.id_UserFlollowing)
