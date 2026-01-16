from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.utils import timezone
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Student(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('college_staff', 'College Staff'),
    )

    DEPARTMENT_CHOICES = (
        ('computer', 'Computer'),
        ('economics', 'Economics'),
        ('english', 'English'),
        ('mathematics', 'Mathematics'),
        ('chemistry', 'Chemistry'),
        
    )

    STUDENT_GRADE = (
        ('fsc 1st year', 'Fsc 1st year'),
        ('fsc 2nd year', 'Fsc 2nd year'),
        ('bachelor', 'Bachelor'),
    )

    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='student',null=True, blank=True)
    department = models.CharField(max_length=30, choices=DEPARTMENT_CHOICES, null=True, blank=True)
    student_grade = models.CharField(max_length=15, choices=STUDENT_GRADE,null=True, blank=True)


    photo = models.ImageField(upload_to='images')
    student_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True)
    contact = models.CharField(max_length=20, null=True)
    roll_no = models.CharField(max_length=20)
    session =  models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=150)
    gender = models.CharField(max_length=10)
    emergency_contact = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5)
    qr_code = models.ImageField(upload_to='qrcodes', blank=True)
    card_issue_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    id_card_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.student_name

    def save(self, *args, **kwargs):
        if not self.pk:
            # New student, generate QR code
            qr_image = qrcode.make(self.roll_no)
            qr_offset = Image.new('RGB', (310, 310), 'white')
            qr_offset.paste(qr_image)
            qr_code_file_name = f'{self.student_name}_qr.png'
            stream = BytesIO()
            qr_offset.save(stream, 'PNG')
            self.qr_code.save(qr_code_file_name, File(stream), save=False)
            qr_offset.close()
        else:
            try:
                old_student = Student.objects.get(pk=self.pk)
                if old_student.roll_no != self.roll_no:
                    # Only generate a new QR code if the ID card number has changed
                    qr_image = qrcode.make(self.roll_no)
                    qr_offset = Image.new('RGB', (310, 310), 'white')
                    qr_offset.paste(qr_image)
                    qr_code_file_name = f'{self.student_name}_qr.png'
                    stream = BytesIO()
                    qr_offset.save(stream, 'PNG')
                    self.qr_code.save(qr_code_file_name, File(stream), save=False)
                    qr_offset.close()
            except Student.DoesNotExist:
                pass  # It's a new student, no need to compare old values

        super(Student, self).save(*args, **kwargs)

@receiver(pre_delete, sender=Student)
def delete_student_images(sender, instance, **kwargs):
    # Delete the associated images
    if instance.photo:
        instance.photo.delete(save=False)
    if instance.qr_code:
        instance.qr_code.delete(save=False)
