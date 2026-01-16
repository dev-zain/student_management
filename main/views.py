from django.shortcuts import redirect, render
from .models import Student
from .forms import StudentForm
from django.db.models import Q
import json
import csv
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Count


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url='login')
def home(request):
    search_query = request.GET.get('search')
    students_list = Student.objects.all()

    if search_query:
        students_list = students_list.filter(
            Q(student_name__icontains=search_query) | Q(department__icontains=search_query) | Q(roll_no__icontains=search_query)
        )

    paginator = Paginator(students_list, 5)  # Show 5 students per page

    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        students = paginator.page(paginator.num_pages)

    context = {
        'students': students,
    }
    return render(request, 'main/home.html', context)



@login_required(login_url='login')
def generate_card(request,pk):
    student = Student.objects.get(id=pk)

    context = {
        'student' : student,
    }
    return render(request,'main/generate_card.html',context)

@login_required(login_url='login')
def full_details(request,pk):
    student = Student.objects.get(id=pk)

    context = {
        'student' : student,
    }
    return render(request,'main/full_details.html',context)

@login_required(login_url='login')
def update_student(request, pk):
    student = Student.objects.get(id=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentForm(instance=student)

    context = {
        'form': form,
        'student': student,
    }

    return render(request, 'main/update_student.html', context)

@login_required(login_url='login')
def delete_student(request,pk):
    student = Student.objects.get(id=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('home')
    
    context = {
        'student' : student,
    }
    return render(request,'main/delete_student.html',context)


@login_required(login_url='login')
def add_user(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentForm()

    context = {
        'form': form,
    }

    return render(request, 'main/add_user.html', context)

    
@login_required(login_url='login')
@login_required(login_url='login')
def identify(request):
    """
    Renders the frontend camera page.
    """
    return render(request, 'main/identify.html')

@login_required(login_url='login')
def process_qr(request):
    """
    Receives QR data from frontend via AJAX.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qr_text = data.get('qr_data')
            
            student = Student.objects.get(roll_no=qr_text)
            
            return JsonResponse({
                'status': 'success',
                'student': {
                    'name': student.student_name,
                    'department': student.department,
                    'roll_no': student.roll_no
                }
            })
            
        except Student.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Student not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required(login_url='login')
def export_students_csv(request):
    """
    Export all students to CSV file
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Name', 'Father Name', 'Roll No', 'Department', 
        'Grade', 'Contact', 'Email', 'Gender', 
        'Blood Group', 'DOB', 'Address'
    ])
    
    students = Student.objects.all()
    for student in students:
        writer.writerow([
            student.student_name,
            student.father_name,
            student.roll_no,
            student.department,
            student.student_grade,
            student.contact,
            student.email,
            student.gender,
            student.blood_group,
            student.dob,
            student.address
        ])
    
    return response


@login_required(login_url='login')
def dashboard(request):
    """
    Dashboard with statistics
    """
    total_students = Student.objects.count()
    by_department = Student.objects.values('department').annotate(count=Count('id'))
    by_role = Student.objects.values('role').annotate(count=Count('id'))
    by_grade = Student.objects.values('student_grade').annotate(count=Count('id'))
    
    context = {
        'total_students': total_students,
        'by_department': by_department,
        'by_role': by_role,
        'by_grade': by_grade,
    }
    
    return render(request, 'main/dashboard.html', context)


@login_required(login_url='login')
def students_by_department(request, department):
    """
    View students filtered by department
    """
    students_list = Student.objects.filter(department=department)
    
    paginator = Paginator(students_list, 10)
    page = request.GET.get('page')
    
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    
    context = {
        'students': students,
        'department': department,
        'total_count': students_list.count(),
    }
    
    return render(request, 'main/department_students.html', context)



