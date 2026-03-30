from django.db import models


class University(models.Model):
    name         = models.CharField(max_length=255)
    programs     = models.JSONField(default=list, blank=True)
    research_groups = models.JSONField(default=list, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'universities'
        verbose_name = 'Universidad'
        verbose_name_plural = 'Universidades'

    def __str__(self):
        return self.name


class Student(models.Model):
    AVAILABILITY_CHOICES = [
        ('full_time',  'Tiempo completo'),
        ('part_time',  'Medio tiempo'),
        ('weekends',   'Fines de semana'),
        ('remote',     'Remoto'),
    ]

    gateway_user_id = models.BigIntegerField(unique=True)
    university      = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True)
    first_name      = models.CharField(max_length=100, blank=True)
    last_name       = models.CharField(max_length=100, blank=True)
    phone           = models.CharField(max_length=20, blank=True)
    academic_info   = models.JSONField(default=dict, blank=True)
    skills          = models.JSONField(default=list, blank=True)
    certifications  = models.JSONField(default=list, blank=True)
    languages       = models.JSONField(default=list, blank=True)
    availability    = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, blank=True)
    portfolio_url   = models.URLField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students'
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Company(models.Model):
    SIZE_CHOICES = [
        ('micro',  'Micro (1-10)'),
        ('small',  'Pequeña (11-50)'),
        ('medium', 'Mediana (51-200)'),
        ('large',  'Grande (200+)'),
    ]

    gateway_user_id = models.BigIntegerField(unique=True)
    name            = models.CharField(max_length=255)
    sector          = models.CharField(max_length=100, blank=True)
    size            = models.CharField(max_length=10, choices=SIZE_CHOICES, blank=True)
    description     = models.TextField(blank=True)
    website         = models.URLField(blank=True)
    reputation      = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'companies'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.name


class GovernmentEntity(models.Model):
    gateway_user_id = models.BigIntegerField(unique=True)
    name            = models.CharField(max_length=255)
    authorized      = models.BooleanField(default=False)
    description     = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'government_entities'
        verbose_name = 'Entidad Gubernamental'
        verbose_name_plural = 'Entidades Gubernamentales'

    def __str__(self):
        return self.name