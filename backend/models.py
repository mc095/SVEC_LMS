from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from datetime import date

class Department(models.Model):
    dept = models.CharField(max_length=255)

    def __str__(self):
        return self.dept 

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses', null=True)  # Changed to nullable
    description = models.TextField(max_length=300)
    image = models.ImageField(upload_to='courses/images')

    def __str__(self):
        return self.course_name

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField(max_length=500,null=True)  # Using EmbedVideoField to store video URLs

    dept = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='videos', null=True)
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos', null=True)
    
    description = models.TextField(blank=True)
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.title

class CustomUserManager(BaseUserManager):
    def _create_user(self, rollno, password=None, **extra_fields):
        if not rollno:
            raise ValueError("The ID is required")
        
        user = self.model(rollno=rollno, **extra_fields)     
        user.set_password(password)
        user.save(using=self._db)  # Use _db to reference the correct database
        return user

    def create_user(self, rollno, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(rollno, password, **extra_fields)

    def create_superuser(self, rollno, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(rollno, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(**{'rollno': username})  # id corresponds to 'rollno'


class Lms_Users(AbstractBaseUser, PermissionsMixin):
    username = None  # We are not using the default username field
    rollno = models.CharField(max_length=100, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=128)

    # Set the custom manager
    objects = CustomUserManager()

    # Define the unique identifier for the user
    USERNAME_FIELD = 'rollno'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name
