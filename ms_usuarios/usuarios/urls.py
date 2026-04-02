from django.urls import path
from . import views

urlpatterns = [
    # Perfil genérico
    path('profiles/', views.create_profile, name='create_profile'),

    # Estudiantes
    path('students/', views.students, name='students'),
    path('students/<int:gateway_user_id>/', views.get_student, name='get_student'),
    path('students/<int:gateway_user_id>/update/', views.update_student, name='update_student'),

    # Universidades
    path('universities/', views.universities, name='universities'),
    path('universities/<int:pk>/', views.get_university, name='get_university'),
    path('universities/<int:pk>/update/', views.update_university, name='update_university'),

    # Empresas
    path('companies/', views.companies, name='companies'),
    path('companies/<int:gateway_user_id>/', views.get_company, name='get_company'),
    path('companies/<int:gateway_user_id>/update/', views.update_company, name='update_company'),

    # Entidades gubernamentales
    path('government-entities/', views.government_entities, name='government_entities'),
    path('government-entities/<int:gateway_user_id>/', views.get_government_entity, name='get_government_entity'),
    path('government-entities/<int:gateway_user_id>/update/', views.update_government_entity, name='update_government_entity'),
]