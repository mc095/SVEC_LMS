from django.shortcuts import render,get_object_or_404,redirect
from backend.models import *
from django.http import HttpResponse
from .forms import *
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            # user = Lms_Users.objects.get(rollno=username)
            # if user.password == password:
            user = authenticate(request, rollno=username, password=password)
            login(request,user)
            courses = Course.objects.all()
            departments = Department.objects.all()
            videos=Video.objects.all()
            context = {
                'courses': courses,
                'departments': departments,
                'videos':videos,
                'username':username,
            }
            response = render(request, 'frontend/home_page.html', context)
            response.set_cookie('username', username)  # Lasts until browser is closed
            return response
            # else:
            #     messages.error(request, "Incorrect Password")  # Add flash message
        except Lms_Users.DoesNotExist:
            messages.error(request, "User not found.")
    return render(request,'frontend/login.html')
    

@login_required(login_url='/')
def home(request):
    courses = Course.objects.all()
    username = request.COOKIES.get('username')
    departments = Department.objects.all()
    videos=Video.objects.all()
    context = {
        'courses': courses,
        'departments': departments,
        'videos':videos,
        'username':username,
    }
    response = render(request, 'frontend/home_page.html', context) 
    return response


@login_required(login_url='/')
def about(request):
    return render(request,'frontend/about.html')

@login_required(login_url='login_page')
def profile(request):
    username = request.COOKIES.get('username')
    if username:
       student = Lms_Users.objects.get(rollno=username)
    else:
         student=None
    return render(request,'frontend/profile.html',{'student':student})


def logout_page(request):
    logout(request)
    return redirect('/') 

@login_required(login_url='login_page')
def course_details(request,course_name):
    videos = Video.objects.all()
    return render(request,'frontend/fetch_course_videos.html',{'videos':videos})

@login_required(login_url='/')
def fetch_course_videos(request,course_name):
    course = Course.objects.get(course_name=course_name)
    # Filter videos based on the selected department and course
    get_course = get_object_or_404(Course, course_name=course_name)
    
    # Filter videos related to the selected course using the correct relationship
    videos = Video.objects.filter(course_name=get_course) 
    # Filtering by selected course
    #current_url = Video.objects.get(title=course_name)
    context = {
        'videos': videos,
        'course': course,
        'title':course_name,

    }

    return render(request, 'frontend/fetch_course_videos.html', context)

@login_required(login_url='/')
def verifypassword(request):
    if request.method == 'POST':
        old_password = request.POST['oldPassword']
        username = request.COOKIES.get('username')  
        try:
            user = Lms_Users.objects.get(rollno=username)
            if user.check_password(old_password):  # Check if the old password is correct
                return render(request, 'frontend/changepassword.html')
            else:
                messages.error(request, "Old password is incorrect.")  # Add flash message
        except Lms_Users.DoesNotExist:
            messages.error(request, "User not found.")
    return render(request, 'frontend/verifypassword.html')

@login_required(login_url='/')
def changepassword(request):
    if request.method == 'POST':
        newpassword = request.POST['newPassword']
        confirmpassword = request.POST['confirmPassword']

        username = request.COOKIES.get('username')
        try:
            user = Lms_Users.objects.get(rollno=username)
            if newpassword == confirmpassword:
                # Save the new password
                user.set_password(newpassword)
                user.save()
                messages.success(request, "Password changed successfully.")
                logout(request)
                return redirect('/logout_page') 
            else:
                messages.error(request, "Passwords do not match.")
        except Lms_Users.DoesNotExist:
            messages.error(request, "User not found.")

    return render(request, 'frontend/changepassword.html')
