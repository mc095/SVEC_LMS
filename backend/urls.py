from django.urls import path
from . import views

urlpatterns = [
    path('custom-admin/', views.custom_admin_view, name='custom-admin-url'),
]
