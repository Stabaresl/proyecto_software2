from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Company, GovernmentEntity, Student, University
from .serializers import (
    CompanyCreateSerializer,
    CompanySerializer,
    GovernmentEntityCreateSerializer,
    GovernmentEntitySerializer,
    StudentCreateSerializer,
    StudentSerializer,
    UniversitySerializer,
)


# ─── PROFILES ─────────────────────────────────────────────────

@api_view(['POST'])
def create_profile(request):
    role = request.data.get('role')
    if not role:
        return Response({'success': False, 'message': 'El campo role es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer_map = {
        'student':    StudentCreateSerializer,
        'company':    CompanyCreateSerializer,
        'state':      GovernmentEntityCreateSerializer,
    }

    if role not in serializer_map and role != 'university':
        return Response({'success': False, 'message': 'Role inválido.'}, status=status.HTTP_400_BAD_REQUEST)

    if role == 'university':
        serializer = UniversitySerializer(data=request.data)
    else:
        serializer = serializer_map[role](data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)

    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


# ─── STUDENTS ─────────────────────────────────────────────────

@api_view(['GET'])
def list_students(request):
    students = Student.objects.select_related('university').all()
    serializer = StudentSerializer(students, many=True)
    return Response({'success': True, 'data': serializer.data})


@api_view(['GET'])
def get_student(request, gateway_user_id):
    try:
        student = Student.objects.select_related('university').get(gateway_user_id=gateway_user_id)
    except Student.DoesNotExist:
        return Response({'success': False, 'message': 'Estudiante no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = StudentSerializer(student)
    return Response({'success': True, 'data': serializer.data})


@api_view(['PUT'])
def update_student(request, gateway_user_id):
    try:
        student = Student.objects.get(gateway_user_id=gateway_user_id)
    except Student.DoesNotExist:
        return Response({'success': False, 'message': 'Estudiante no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = StudentCreateSerializer(student, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'data': serializer.data})
    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


# ─── UNIVERSITIES ─────────────────────────────────────────────

@api_view(['GET'])
def list_universities(request):
    universities = University.objects.all()
    serializer = UniversitySerializer(universities, many=True)
    return Response({'success': True, 'data': serializer.data})


@api_view(['GET'])
def get_university(request, pk):
    try:
        university = University.objects.get(pk=pk)
    except University.DoesNotExist:
        return Response({'success': False, 'message': 'Universidad no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UniversitySerializer(university)
    return Response({'success': True, 'data': serializer.data})


@api_view(['POST'])
def create_university(request):
    serializer = UniversitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(['PUT'])
def update_university(request, pk):
    try:
        university = University.objects.get(pk=pk)
    except University.DoesNotExist:
        return Response({'success': False, 'message': 'Universidad no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UniversitySerializer(university, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'data': serializer.data})
    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


# ─── COMPANIES ────────────────────────────────────────────────

@api_view(['GET'])
def list_companies(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response({'success': True, 'data': serializer.data})


@api_view(['GET'])
def get_company(request, gateway_user_id):
    try:
        company = Company.objects.get(gateway_user_id=gateway_user_id)
    except Company.DoesNotExist:
        return Response({'success': False, 'message': 'Empresa no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CompanySerializer(company)
    return Response({'success': True, 'data': serializer.data})


@api_view(['PUT'])
def update_company(request, gateway_user_id):
    try:
        company = Company.objects.get(gateway_user_id=gateway_user_id)
    except Company.DoesNotExist:
        return Response({'success': False, 'message': 'Empresa no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CompanyCreateSerializer(company, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'data': serializer.data})
    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


# ─── GOVERNMENT ENTITIES ──────────────────────────────────────

@api_view(['GET'])
def list_government_entities(request):
    entities = GovernmentEntity.objects.all()
    serializer = GovernmentEntitySerializer(entities, many=True)
    return Response({'success': True, 'data': serializer.data})


@api_view(['GET'])
def get_government_entity(request, gateway_user_id):
    try:
        entity = GovernmentEntity.objects.get(gateway_user_id=gateway_user_id)
    except GovernmentEntity.DoesNotExist:
        return Response({'success': False, 'message': 'Entidad no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = GovernmentEntitySerializer(entity)
    return Response({'success': True, 'data': serializer.data})


@api_view(['PUT'])
def update_government_entity(request, gateway_user_id):
    try:
        entity = GovernmentEntity.objects.get(gateway_user_id=gateway_user_id)
    except GovernmentEntity.DoesNotExist:
        return Response({'success': False, 'message': 'Entidad no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = GovernmentEntityCreateSerializer(entity, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True, 'data': serializer.data})
    return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)