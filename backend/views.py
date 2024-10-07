from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import *
import firebase_admin
from firebase_admin import credentials, storage
import pandas as pd
# Create your views here.

import os
import firebase_admin
from firebase_admin import credentials

# Load Firebase configuration from environment variables
firebase_config = {
    "type": os.environ.get('TYPE'),
    "project_id": os.environ.get('PROJECT_ID'),
    "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
    "private_key": os.environ.get('PRIVATE_KEY'),
    "client_email": os.environ.get('CLIENT_EMAIL'),
    "client_id": os.environ.get('CLIENT_ID'),
    "auth_uri": os.environ.get('AUTH_URI'),
    "token_uri": os.environ.get('TOKEN_URI'),
    "auth_provider_x509_cert_url": os.environ.get('AUTH_PROVIDER_CERT_URL'),
    "client_x509_cert_url": os.environ.get('CLIENT_CERT_URL')
}

# Initialize Firebase Admin SDK with environment-based credentials
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'svec-lms.appspot.com'
})

def add_video(request):
    form = CustomAdminForm(request.POST, request.FILES)
    if request.method=='POST':
        if form.is_valid():
            video_file = request.FILES['video']
            dept_id = form.cleaned_data['department']
            course_name = form.cleaned_data['course']
            description = request.POST['description']
            if dept_id is None or course_name is None or description is None:
                return HttpResponse("Missing POST data.")

        try:
            course = Course.objects.get(course_name=course_name)
        except Course.DoesNotExist:
            # Create a new course if it doesn't exist in the database
            course = Course.objects.create(course_name=course_name)  # Adjust as per your Course model

        # Define the folder path for the course
        course_folder = f"videos/{course.course_name}/"  # Assuming course.name is the folder name

        # Check if the folder exists in Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(course_folder)  # Create a blob for the folder
        if not blob.exists():  # Check if the folder already exists
            blob.upload_from_string('')  # Create an empty folder

        bucket = storage.bucket()
        # Create a blob for the video file
        video_blob = bucket.blob(course_folder + video_file.name)
        # Upload the video file to Firebase Storage
        video_blob.upload_from_file(video_file, content_type=video_file.content_type)

        video_blob.make_public()
        # Get the public URL of the uploaded video
        public_url=video_blob.public_url

        s = Video(video_url=public_url,title=video_file.name,dept=Department.objects.get(dept=dept_id),course_name=Course.objects.get(course_name=course_name),description=description)
        s.save()
        return redirect('admin/backend/video/')
    return render(request,'upload.html',{'form': form})


def course_upload(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            course = form.save(commit=False)  # Do not save yet
            
            # Handle the image upload
            if request.FILES.get('image'):
                course.image = request.FILES['image'].read()  # Read the image as binary data
            
            course.save()  # Now save the instance
            return redirect('some_view_name')  # Redirect after success
    else:
        form = CourseForm()
    
    return render(request,'couse_uplod.html',{'form':form})


@staff_member_required  
def custom_admin_view(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["excel_file"]
            try:
                df = pd.read_excel(excel_file)
                for index, row in df.iterrows():
                    user = Lms_Users(
                        rollno=row['Htno'],  
                        name=row['Name'],
                        branch=row['Branch'],
                    )
                    # Set the Aadhar number as the password, but don't store it directly
                    user.set_password(str(row['AadharNumber']))  # AadharNumber column is used as password
                    user.save()
                    
                return redirect('admin/backend/lms_users/')
            except Exception as e:
                return HttpResponse(f"Error processing file: {str(e)}")
    else:
        form = ExcelUploadForm()

    return render(request, "admin/users_upload.html", {"form": form})


def custom_action_view(request):
    return HttpResponse("Custom button clicked!")


