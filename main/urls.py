from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('generate-card/<str:pk>/',views.generate_card,name='generate_card'),
    path('full-details/<str:pk>/',views.full_details,name='full_details'),
    path('update-student/<str:pk>/',views.update_student,name='update_student'),
    path('delete-student/<str:pk>/',views.delete_student,name='delete_student'),
    path('add-user/',views.add_user,name='add_user'),
    path('auth/',views.identify,name='identify'),
    path('process_qr/',views.process_qr,name='process_qr'),
    path('export-csv/',views.export_students_csv,name='export_csv'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('department/<str:department>/',views.students_by_department,name='department_students'),
    
]