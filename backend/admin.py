from django.contrib import admin
from .models import *
from django.http import HttpResponse
from django.urls import path
from . import views
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Lms_Users
from .forms import UserChangeForm,UserCreationForm
# Register your models here.


def custom_button_action(modeladmin, request, queryset):
    # Perform your custom action here
    return HttpResponse("Button clicked!")


custom_button_action.short_description = "Custom Button Action"


class VideoAdmin(admin.ModelAdmin):   

    actions = [custom_button_action]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            # Redirect or block the 'add' URL
            path('add/', self.admin_site.admin_view(views.add_video)),
        ]
        return custom_urls + urls
    
class CourseAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload/', self.admin_site.admin_view(views.course_upload), name='course_upload'),
        ]
        return custom_urls + urls


class LmsUsersAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('rollno', 'name', 'branch', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('rollno', 'password')}),
        ('Personal info', {'fields': ('name', 'branch')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('rollno', 'name', 'branch', 'password1', 'password2'),
        }),
    )
    search_fields = ('rollno',)
    ordering = ('rollno',)
    filter_horizontal = ()

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('custom-view/', self.admin_site.admin_view(views.custom_admin_view), name="custom-view"),
        ]
        return custom_urls + urls


# Now register the new Lms_UsersAdmin
admin.site.register(Lms_Users, LmsUsersAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Department)
admin.site.register(Video,VideoAdmin)
