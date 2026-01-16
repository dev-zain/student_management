from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Student
from datetime import date
import json


class StudentModelTest(TestCase):
    """Test cases for the Student model"""
    
    def setUp(self):
        """Create a test student"""
        self.student = Student.objects.create(
            role='student',
            department='computer',
            student_grade='fsc 1st year',
            student_name='Test Student',
            father_name='Test Father',
            dob=date(2000, 1, 1),
            contact='1234567890',
            roll_no='CS-2024-001',
            session='2024-2025',
            email='test@example.com',
            address='123 Test Street',
            gender='Male',
            emergency_contact='0987654321',
            blood_group='O+',
            id_card_number='ID-001'
        )
    
    def test_student_creation(self):
        """Test that a student can be created successfully"""
        self.assertEqual(self.student.student_name, 'Test Student')
        self.assertEqual(self.student.roll_no, 'CS-2024-001')
        self.assertEqual(self.student.department, 'computer')
    
    def test_student_str_method(self):
        """Test the string representation of a student"""
        self.assertEqual(str(self.student), 'Test Student')
    
    def test_qr_code_generation(self):
        """Test that QR code is generated on student creation"""
        # QR code should be generated automatically
        self.assertTrue(self.student.qr_code)
        self.assertIn('Test_Student_qr', self.student.qr_code.name)
    
    def test_student_ordering(self):
        """Test that students are ordered by creation date (newest first)"""
        student2 = Student.objects.create(
            student_name='Second Student',
            father_name='Second Father',
            roll_no='CS-2024-002',
            session='2024-2025',
            address='456 Test Ave',
            gender='Female',
            emergency_contact='1112223333',
            blood_group='A+',
            id_card_number='ID-002'
        )
        students = Student.objects.all()
        self.assertEqual(students[0], student2)  # newest first


class StudentViewsTest(TestCase):
    """Test cases for Student views"""
    
    def setUp(self):
        """Create test user and student"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            is_superuser=True
        )
        self.student = Student.objects.create(
            student_name='View Test Student',
            father_name='Test Father',
            roll_no='CS-2024-003',
            session='2024-2025',
            address='789 Test Blvd',
            gender='Male',
            emergency_contact='5556667777',
            blood_group='B+',
            id_card_number='ID-003'
        )
    
    def test_home_view_redirect_if_not_logged_in(self):
        """Test that home view redirects to login if user is not authenticated"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertIn('/login', response.url)
    
    def test_home_view_accessible_when_logged_in(self):
        """Test that home view is accessible after login"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View Test Student')
    
    def test_search_functionality(self):
        """Test that search works correctly"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'), {'search': 'View Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View Test Student')
    
    def test_process_qr_with_valid_student(self):
        """Test QR processing with a valid roll number"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('process_qr'),
            data=json.dumps({'qr_data': 'CS-2024-003'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['student']['name'], 'View Test Student')
    
    def test_process_qr_with_invalid_student(self):
        """Test QR processing with an invalid roll number"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('process_qr'),
            data=json.dumps({'qr_data': 'INVALID-ROLL'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'error')


class StudentCRUDTest(TestCase):
    """Test Create, Read, Update, Delete operations"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='admin',
            password='admin123',
            is_superuser=True
        )
        self.client.login(username='admin', password='admin123')
    
    def test_delete_student(self):
        """Test that a student can be deleted"""
        student = Student.objects.create(
            student_name='Delete Test',
            father_name='Test Father',
            roll_no='CS-2024-999',
            session='2024-2025',
            address='Delete St',
            gender='Male',
            emergency_contact='9998887777',
            blood_group='AB+',
            id_card_number='ID-999'
        )
        count_before = Student.objects.count()
        response = self.client.post(reverse('delete_student', args=[student.id]))
        count_after = Student.objects.count()
        
        self.assertEqual(count_after, count_before - 1)
        self.assertEqual(response.status_code, 302)  # Redirect after delete
