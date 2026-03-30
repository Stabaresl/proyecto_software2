from rest_framework import serializers
from .models import Student, University, Company, GovernmentEntity


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model  = University
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    university_name = serializers.CharField(source='university.name', read_only=True)

    class Meta:
        model  = Student
        fields = '__all__'


class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Student
        fields = [
            'gateway_user_id',
            'university',
            'first_name',
            'last_name',
            'phone',
            'academic_info',
            'skills',
            'certifications',
            'languages',
            'availability',
            'portfolio_url',
        ]

    def validate_gateway_user_id(self, value):
        if Student.objects.filter(gateway_user_id=value).exists():
            raise serializers.ValidationError('Ya existe un perfil con este usuario.')
        return value


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Company
        fields = '__all__'


class CompanyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Company
        fields = [
            'gateway_user_id',
            'name',
            'sector',
            'size',
            'description',
            'website',
        ]

    def validate_gateway_user_id(self, value):
        if Company.objects.filter(gateway_user_id=value).exists():
            raise serializers.ValidationError('Ya existe un perfil con este usuario.')
        return value


class GovernmentEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model  = GovernmentEntity
        fields = '__all__'


class GovernmentEntityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = GovernmentEntity
        fields = [
            'gateway_user_id',
            'name',
            'description',
        ]

    def validate_gateway_user_id(self, value):
        if GovernmentEntity.objects.filter(gateway_user_id=value).exists():
            raise serializers.ValidationError('Ya existe un perfil con este usuario.')
        return value