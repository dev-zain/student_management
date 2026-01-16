from rest_framework import serializers, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model"""
    
    class Meta:
        model = Student
        fields = [
            'id', 'role', 'department', 'student_grade',
            'photo', 'student_name', 'father_name', 'dob',
            'contact', 'roll_no', 'session', 'email',
            'address', 'gender', 'emergency_contact',
            'blood_group', 'qr_code', 'card_issue_date',
            'expiry_date', 'id_card_number', 'created_at', 'updated_at'
        ]
        read_only_fields = ['qr_code', 'created_at', 'updated_at']


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Student CRUD operations
    
    Endpoints:
    - GET /api/students/ - List all students
    - POST /api/students/ - Create a new student
    - GET /api/students/{id}/ - Retrieve a specific student
    - PUT /api/students/{id}/ - Update a student
    - DELETE /api/students/{id}/ - Delete a student
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def get_queryset(self):
        """Allow filtering by department and role"""
        queryset = Student.objects.all()
        department = self.request.query_params.get('department', None)
        role = self.request.query_params.get('role', None)
        
        if department:
            queryset = queryset.filter(department=department)
        if role:
            queryset = queryset.filter(role=role)
        
        return queryset


@api_view(['GET'])
def student_stats(request):
    """
    Get statistics about students
    
    Returns:
    - Total count
    - Count by department
    - Count by role
    """
    from django.db.models import Count
    
    total = Student.objects.count()
    by_department = Student.objects.values('department').annotate(count=Count('id'))
    by_role = Student.objects.values('role').annotate(count=Count('id'))
    
    return Response({
        'total_students': total,
        'by_department': list(by_department),
        'by_role': list(by_role)
    })
