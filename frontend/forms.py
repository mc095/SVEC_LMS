from django import forms

class StudentIDLoginForm(forms.Form):
    rollnumber = forms.CharField(label="Roll Number", max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)