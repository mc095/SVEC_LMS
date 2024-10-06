from django import forms
from .models import *
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class CustomAdminForm(forms.Form):
    video = forms.FileField(label='Upload Video') 
    description = forms.CharField(widget=forms.Textarea, label='Description')
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label='Course', widget=forms.Select)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), label='Department', widget=forms.Select)


class CourseForm(forms.ModelForm):
    image = forms.FileField(required=True)  # Use a file field for image uploads

    class Meta:
        model = Course
        fields = ['course_name', 'dept', 'description', 'image'] 

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Lms_Users
        fields = ('rollno', 'name', 'branch', 'password', 'is_active', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here so that the password is not changed in the admin.
        return self.initial["password"]
    

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Lms_Users
        fields = ('rollno', 'name', 'branch')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()
