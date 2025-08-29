"""
URL configuration for smart_attendance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from attendance import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("students/", views.student_list, name="student_list"),
    path("upload/", views.upload_pdf, name="upload_pdf"),
    path("schedule_class/", views.schedule_class, name="schedule_class"),
    path("delete_class/<int:pk>/", views.delete_class, name="delete_class"), # New URL for deleting classes
    path("mark_attendance/", views.mark_attendance, name="mark_attendance"),
    path("student/edit/<int:pk>/", views.student_edit, name="student_edit"), # New URL for editing students
    path("student/delete/<int:pk>/", views.student_delete, name="student_delete"), # New URL for deleting students
]

