from django.urls import path
from . import views

urlpatterns = [
    path('course/create/', views.create_course, name='create_course'),
    path('course/get/<str:alias>/', views.get_course, name='get_course'),
    path('course/update/<str:alias>/', views.update_course, name='update_course'),
    path('course/delete/<str:alias>/', views.delete_course, name='delete_course'),
]
