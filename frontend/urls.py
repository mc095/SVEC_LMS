from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.login_page,name='login_page'),
    path('home/',views.home,name='home'),
    #path('course/<str:title>', views.fetch_course_videos, name='fetch_course_videos'),
    path('course/<str:course_name>', views.fetch_course_videos, name='fetch_course_videos'),
    path('about/',views.about,name='about'),
    path('profile/',views.profile,name='profile'),
    path('logout_page/',views.logout_page,name='logout_page'),
    path('verifypassword/',views.verifypassword,name='verifypassword'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('course_details/<str:course_name>',views.course_details,name='course_details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
