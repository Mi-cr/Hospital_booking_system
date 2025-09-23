from django.shortcuts import render,redirect,get_object_or_404 
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
import secrets
import string
from django.contrib.auth.models import auth 
from django.contrib.auth import authenticate, login 
from django.shortcuts import render, redirect
from .models import CustomUser, Patient, depatment,doctor,Appointment
from django.contrib import messages
from django.http import HttpResponse
import random
from django.db.models import Q 
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import Http404
from datetime import datetime, timedelta
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from collections import defaultdict

from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
import re


# Create your views here
def homepage(request):
    return render(request,'home2.html')
def patientsignup(request):
    return render(request,'usersignup.html')
def loginpage(request):
    return render(request,'login.html')
def addpatient(request):

    pending_doctor_approvals = doctor.objects.filter(user__status=0).count()


    pending_approvals = Appointment.objects.filter(status="Pending").count()


    return render(request, 'addpatint.html', {
        'pending_doctor_approvals': pending_doctor_approvals,
        'pending_approvals': pending_approvals
    })



def adminhome(request):

    total_patients = Patient.objects.count()


    total_doctors = doctor.objects.filter(user__status=1).count()

    pending_approvals = Appointment.objects.filter(status="Pending").count()
    pending_doctor_approvals = doctor.objects.filter(user__status=0).count()

    
    context = {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "pending_approvals": pending_approvals,
        "pending_doctor_approvals": pending_doctor_approvals
    }
    return render(request, "adminhome.html", context)
def patienthome(request):
    return render(request,'patienthome.html')
def loginpage(request):
    return render(request,'login.html')


def generate_random_string():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(secrets.choice(alphabet) for i in range(2))  
    return random_string



def generate_password():

    password = ''.join(random.choices(string.digits, k=6))  # 6 random digits

    return password
def patientform(request):
    return render(request,'usersignup.html')

# Register patient function
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def register_patient(request):
    if request.method == "POST":
        username = request.POST.get('username')  
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        user_type = request.POST.get('text')  
        age = request.POST.get('age')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        contact = request.POST.get('phone')
        profile_picture = request.FILES.get('profile-picture')

    
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format. Please enter a valid email address.")
            return redirect('patientform')


        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different email address.")
            return redirect('patientform')

        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('patientform')

    
        if not contact.isdigit() or len(contact) != 10:
            messages.error(request, "Invalid phone number. Please enter a valid 10-digit phone number.")
            return redirect('patientform')

    
        random_string = generate_random_string()
        patient_id = f"{first_name[:3].lower()}{random_string}"

    
        password = generate_password()

        
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            user_type=user_type
        )
        user.save()

        # Create the patient profile
        patient = Patient.objects.create(
            user=user,
            age=age,
            address=address,
            Gender=gender,
            contact=contact,
            image=profile_picture,
            patient_id=patient_id 
        )
        patient.save()

        
        subject = "Patient Registration Details"
        message = f"""
        Dear {first_name} {last_name},

        Your registration is successful!

        Username: {username}
        Patient ID: {patient_id}
        Password: {password}

        Please log in to your account with your credentials.

        Best Regards,
        Apollo Hospital
        """
        recipient_list = [email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

        messages.success(request, "Patient registered successfully! An email has been sent with your credentials.")
        return redirect('patientform')

    return redirect('patientform')

def login1(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user=authenticate(username=username,password=password)
    

        if user is not None:
            if user.user_type == '1':
                login(request,user)
                return redirect('adminhome')
            elif user.user_type == '2':
                auth.login(request,user)
                return redirect('patienthome')
            elif user.user_type == '3':
                auth.login(request,user)
                return redirect('doctorhomepage')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('loginpage')
    
    return redirect('loginpage')
def adddept(request):

    pending_approvals = Appointment.objects.filter(status="Pending").count()

    pending_doctor_approvals = doctor.objects.filter(user__status=0).count()

    
    context = {
        "pending_approvals": pending_approvals,
        "pending_doctor_approvals": pending_doctor_approvals,
    }

    return render(request, 'departmentadd.html', context)
def add_department(request):
    if request.method == "POST":
    
        department_name = request.POST.get("department_name")
        description = request.POST.get("description")
        
    
        if department_name and description:
            depatment.objects.create(DepatmentName=department_name, Description=description)
            messages.success(request, "Department added successfully!")
            return redirect("adddept") 
        else:
            messages.error(request, "Please fill in all fields.")
    
    
    return render(request, "adddept") 
def doctorsignup(request):
    depatments=depatment.objects.all()
    return render(request,'doctregister.html',{'dept':depatments})
def doctorsignupdetail(request):
    if request.method == 'POST':
    
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        username = request.POST.get('username')  
        email = request.POST.get('email')
        user_type = request.POST.get('text')  
        age = request.POST.get('age')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        specialization_id = request.POST.get('specialization')
        profile_picture = request.FILES.get('profile-picture')

    
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format. Please enter a valid email address.")
            return redirect('doctorsignup')

        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different email address.")
            return redirect('doctorsignup')

    
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('doctorsignup')

        
        if not re.fullmatch(r'\d{10}', phone):
            messages.error(request, "Invalid phone number. Please enter a valid 10-digit phone number.")
            return redirect('doctorsignup')

        
        try:
            specialization = depatment.objects.get(id=specialization_id)
        except depatment.DoesNotExist:
            messages.error(request, "Invalid department selected.")
            return redirect('doctorsignup')

        
        user = CustomUser.objects.create_user(
            username=username, 
            email=email, 
            first_name=first_name, 
            last_name=last_name,
            user_type=user_type
        )
        user.save()

        
        new_doctor = doctor(
            user=user,
            Department=specialization,
            Address=address,
            Age=age,
            Contact=phone,
            Image=profile_picture
        )
        new_doctor.save()

    
        messages.success(request, 'Registration successful!please wait  for  approval.')

        return redirect('doctorsignup') 

    return render(request, 'doctorsignup.html') 

def doctor_list(request):
    
    doctors = doctor.objects.select_related('user').all()  


    pending_doctor_approvals = doctor.objects.filter(user__status=0).count()


    pending_approvals = Appointment.objects.filter(status="Pending").count()

    
    return render(request, 'doctorapprove.html', {
        'doctors': doctors,
        'pending_doctor_approvals': pending_doctor_approvals,
        'pending_approvals': pending_approvals
    })

def generate_password():
    
    password = ''.join(random.choices(string.digits, k=6))  

    return password


def approve_doctor(request, id):

    doctor_instance = get_object_or_404(doctor, id=id)

    user = doctor_instance.user


    if user.status == 1:
        messages.warning(request, "This doctor is already approved.")
        return redirect('doctor_list')

    
    password = generate_password()


    user.set_password(password)  
    user.status = 1  
    user.save() 


    subject = "Approval Notification - Your Login Credentials"
    message = (
        f"Dear Dr. {user.first_name} {user.last_name},\n\n"
        f"Congratulations! Your account has been approved.\n"
        f"Here are your login credentials:\n"
        f"Username: {user.username}\n"
        f"Password: {password}\n\n"
        f"Please log in to your account and change your password for security purposes.\n\n"
        f"Best regards,\n"
        f"Hospital Admin Team"
    )
    recipient_list = [user.email]
    
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        messages.success(request, f"Doctor {user.first_name} {user.last_name} has been approved successfully")
    except Exception as e:
        messages.error(request, f"Doctor {user.first_name} {user.last_name} has been approved, but there was an error sending the email: {str(e)}")


    return redirect('doctor_list')
    

def disapprove_doctor(request, doctor_id):

    doctor_instance = get_object_or_404(doctor, id=doctor_id)
    user = doctor_instance.user


    send_mail(
        'Account Disapproved',
        f'Dear {user.first_name} {user.last_name},\n\n'
        'We regret to inform you that your account has been disapproved and your account has been removed from our system.\n\n'
        'Thank you.',
        settings.EMAIL_HOST_USER,
        [user.email],
    )

    
    doctor_instance.delete()  
    user.delete()            

    
    messages.success(request, f"Doctor {user.first_name} {user.last_name}'s account has been deleted and notified.")
    return redirect('doctor_list')  

@login_required


def doctorhomepage(request):
    
    today = now().date()


    doctor_instance = doctor.objects.filter(user=request.user).first()

    if doctor_instance:
    
        doctor_image = doctor_instance.Image.url if doctor_instance.Image else None
        first_name = doctor_instance.user.first_name
        last_name = doctor_instance.user.last_name
        department_name = doctor_instance.Department.DepatmentName if doctor_instance.Department else "No Department"

        
        total_pending_appointments = Appointment.objects.filter(
            doctor_id=doctor_instance.id,
            consulted=0,  
            status="Approved"  
        ).count()
        pending_appointments_today = Appointment.objects.filter(
            doctor_id=doctor_instance.id,
            consulted=0,  
            status="Approved",  
            appointment_date=today  
        ).count()
    else:
        
        doctor_image = None
        first_name = "N/A"
        last_name = "N/A"
        department_name = "No Department"
        total_pending_appointments = 0
        pending_appointments_today = 0

    return render(request, 'doctorhome.html', {
        'doctor_image': doctor_image,
        'first_name': first_name,
        'last_name': last_name,
        'department_name': department_name,
        'total_pending_appointments': total_pending_appointments,
          'pending_appointments_today': pending_appointments_today  # Pass total pending count
    })


def doctoraddadmin(request):
    
    depatments = depatment.objects.all()


    pending_doctor_approvals = doctor.objects.filter(user__status=0).count()

    
    pending_approvals = Appointment.objects.filter(status="Pending").count()


    return render(request, 'admindoctoradd.html', {
        'dept': depatments,
        'pending_doctor_approvals': pending_doctor_approvals,
        'pending_approvals': pending_approvals
    })

def add_doctor(request):
    if request.method == "POST":
    
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        age = request.POST.get('age')
        address = request.POST.get('address')
        user_type = request.POST.get('text')  
        department_id = request.POST.get('department')
        phone = request.POST.get('phone')
        profile_picture = request.FILES.get('profile_picture')

    
        password = generate_password()

        
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phone_regex = r'^\d{10}$'  

        if not re.match(email_regex, email):
            messages.error(request, "Invalid email format. Please enter a valid email address.")
            return redirect('doctoraddadmin')

        if not re.match(phone_regex, phone):
            messages.error(request, "Invalid phone number format. Please enter a 10-digit phone number.")
            return redirect('doctoraddadmin')

        try:
        
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, " username  already exists.")
                return redirect('doctoraddadmin')

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request,"email already exists")
                return redirect('doctoraddadmin')


            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,  
                user_type=user_type,
            )

        
            user.status = 1
            user.save()

        
            department = depatment.objects.get(id=department_id)

            
            doctor_instance = doctor.objects.create(
                user=user,
                Department=department,
                Address=address,
                Age=age,
                Contact=phone,
                Image=profile_picture,
            )
            doctor_instance.save()

            
            subject = "Account Approved - Login Credentials"
            message = (
                f"Dear Dr. {first_name} {last_name},\n\n"
                f"Your account has been created and approved!\n"
                f"Username: {username}\n"
                f"Password: {password}\n\n"
                f"Please log in and change your password for security reasons.\n\n"
                f"Thank you!"
            )
            recipient_list = [email]
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

            messages.success(request, f"Doctor {first_name} {last_name} added and approved successfully.")
            return redirect('doctoraddadmin')  

        except IntegrityError:
            messages.error(request, "An account with this username or email already exists.")
            return redirect('doctoraddadmin')


    return redirect('doctoraddadmin')





@login_required

def booking_form(request):

    departments = depatment.objects.all()

    approved_doctors = doctor.objects.filter(user__status=1)


    doctors_by_department = defaultdict(list)
    for doc in approved_doctors:
        doctors_by_department[doc.Department].append(doc)

    
    try:
        patient_details = Patient.objects.select_related('user').get(user=request.user)
    except Patient.DoesNotExist:
        patient_details = None

    return render(request, 'appoinment.html', {
        'departments': departments,
        'patient_details': patient_details,
        'doctors_by_department': doctors_by_department,
    })
def get_doctors(request, department_id):
    try:
        
        doctors = doctor.objects.filter(Department_id=department_id, user__status=1)
        
        doctor_data = [
            {"id": doc.id, "name": f"Dr. {doc.user.first_name} {doc.user.last_name}"}
            for doc in doctors
        ]
        return JsonResponse({"doctors": doctor_data})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



def create_booking(request):
    if request.method == 'POST':
        department_id = request.POST.get('department')
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        try:
            
            patient = Patient.objects.get(user=request.user)

        
            existing_appointment = Appointment.objects.filter(
                patient=patient,
                doctor_id=doctor_id,
                appointment_date=appointment_date
            ).exists()

            if existing_appointment:
                messages.error(request, "You already have an appointment with this doctor on the same day.")
                return redirect('booking_form')

        
            daily_appointments = Appointment.objects.filter(
                doctor_id=doctor_id,
                appointment_date=appointment_date
            ).count()

            if daily_appointments >= 5:
                messages.error(request, "This doctor has already reached the maximum number of appointments for the day.")
                return redirect('booking_form')

        
            conflicting_appointment = Appointment.objects.filter(
                doctor_id=doctor_id,
                appointment_date=appointment_date,
                appointment_time=appointment_time
            ).exists()

            if conflicting_appointment:
                messages.error(request, "This time slot is already booked. Please select a different time.")
                return redirect('booking_form')

            
            Appointment.objects.create(
                user=request.user,
                patient=patient,
                doctor_id=doctor_id,
                department_id=department_id,
                appointment_date=appointment_date,
                appointment_time=appointment_time
            )

            messages.success(request, "Appointment booked successfully! Check your email and wait for booking approval.")
            return redirect('booking_form')

        except Patient.DoesNotExist:
            messages.error(request, "Patient details not found.")
            return redirect('booking_form')

def patient_appointments(request):
    
    appointments = Appointment.objects.select_related('patient', 'doctor', 'department') \
                                     .all()  
    
    
    for appointment in appointments:
        if appointment.appointment_time:
            appointment.formatted_time = appointment.appointment_time.strftime("%I:%M %p")  
        else:
            appointment.formatted_time = 'Not set'  
    
    
    pending_doctor_approvals = doctor.objects.filter(user__status=0).count()

    
    pending_approvals = Appointment.objects.filter(status="Pending").count()

    
    return render(request, 'approvepatient.html', {
        'appointments': appointments,
        'pending_doctor_approvals': pending_doctor_approvals,
        'pending_approvals': pending_approvals
    })

def approve_patient(request, appointment_id):
    
    try:
        appointment = get_object_or_404(Appointment, id=appointment_id)
    except Appointment.DoesNotExist:
        messages.error(request, "Appointment not found.")
        return redirect("patient_appointments")  

    
    appointment.status = "Approved"
    appointment.save()

    
    patient_email = appointment.patient.user.email

    
    appointment_time = (
        appointment.appointment_time.strftime('%I:%M %p')
        if appointment.appointment_time
        else 'Not set'
    )

    
    subject = "Appointment Approved"
    message = (
        f"Dear {appointment.patient.user.first_name},\n\n"
        f"Your appointment with Dr. {appointment.doctor.user.first_name} {appointment.doctor.user.last_name} "
        f"has been approved.\n\n"
        f"Details:\n"
        f"Date: {appointment.appointment_date}\n"
        f"Time: {appointment_time}\n\n"
        "Thank you for choosing us.\n"
    )

    
    try:
        send_mail(
            subject,
            message,
            "no-reply@clinic.com",  
            [patient_email],
            fail_silently=False,
        )
        messages.success(request, "Appointment approved successfully.")
    except Exception as e:
        messages.error(request, f"Appointment approved, but email failed: {str(e)}")

    return redirect("patient_appointments")  

def disapprove_patient(request, appointment_id):
    
    appointment = get_object_or_404(Appointment, id=appointment_id)

    
    appointment.status = "Disapproved"
    appointment.save()

    
    patient_email = appointment.patient.user.email


    subject = "Appointment Disapproved"
    message = (
        f"Dear {appointment.patient.user.first_name},\n\n"
        f"Your appointment with Dr. {appointment.doctor.user.first_name} {appointment.doctor.user.last_name} "
        f"on {appointment.appointment_date} has been disapproved.\n\n"
        "Please contact us for further details.\n\n"
        "Thank you."
    )

    
    try:
        if patient_email:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [patient_email],
                fail_silently=False,
            )
        messages.success(request, "Appointment disapproved successfully.")
    except Exception as e:
        messages.error(request, f"Appointment disapproved, but email failed: {str(e)}")

    
    return redirect("patient_appointments")  




from datetime import date

def doctoappointments(request):
    try:
    
        doctor_instance = doctor.objects.get(user=request.user)
        
    
        doctor_image = doctor_instance.Image.url if doctor_instance.Image else None
        first_name = doctor_instance.user.first_name
        last_name = doctor_instance.user.last_name
        department_name = doctor_instance.Department.DepatmentName if doctor_instance.Department else "No Department"

        
        total_pending_appointments = Appointment.objects.filter(
            doctor_id=doctor_instance.id,
            consulted=0, 
            status="Approved" 
        ).count()
    except doctor.DoesNotExist:
    
        doctor_image = None
        first_name = "N/A"
        last_name = "N/A"
        department_name = "No Department"
        doctor_instance = None
        total_pending_appointments = 0

    if doctor_instance:
        
        approved_appointments = Appointment.objects.filter(
            doctor=doctor_instance,
            status="Approved"
        ).order_by('appointment_date', 'appointment_time')  
    else:
        approved_appointments = []

    
    return render(request, 'pdetail.html', {
        'appointments': approved_appointments,
        'doctor_image': doctor_image,
        'first_name': first_name,
        'last_name': last_name,
        'department_name': department_name,
        'total_pending_appointments': total_pending_appointments,  
    })


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Appointment

def toggle_consulted(request, appointment_id):
    """
    Toggle the 'consulted' status of an appointment between 'Consulted' (1) and 'Not Consulted' (0).
    """
    if request.method == "POST":
        
        appointment = get_object_or_404(Appointment, id=appointment_id)

    
        if 'consulted' in request.POST:
            
            appointment.consulted = 1
            status_message = "Consulted"
        elif 'not_consulted' in request.POST:
        
            appointment.consulted = 0
            status_message = "Not Consulted"
        else:
            messages.error(request, "Invalid action.")
            return redirect('doctoappointments')  

        
        appointment.save()

    
        messages.success(request, f"Appointment status updated to '{status_message}'.")

    
    return redirect('doctoappointments')  



from django.db.models import Case, When, Value, CharField
def appointment_list(request):
    
    appointments = Appointment.objects.filter(status='approved').annotate(
        consulted_status=Case(
            When(consulted=1, then=Value("Consulted")),
            When(consulted=0, then=Value("Not Consulted")),
            default=Value("Pending"),
            output_field=CharField()
        )
    )
    
    
    pending_doctor_approvals = doctor.objects.filter(user__status=0).count()


    pending_approvals = Appointment.objects.filter(status="Pending").count()

    
    return render(request, 'consultdetail.html', {
        'appointments': appointments,
        'pending_doctor_approvals': pending_doctor_approvals,
        'pending_approvals': pending_approvals
    })


def logout(request): 
    auth.logout(request) 
    return redirect('loginpage')
def view_patients(request):
    
    patients = Patient.objects.select_related('user').all()

    pending_doctor_approvals = doctor.objects.filter(user__status=0).count()


    pending_approvals = Appointment.objects.filter(status="Pending").count()

    
    return render(request, 'deltpatients.html', {
        'patients': patients,
        'pending_doctor_approvals': pending_doctor_approvals,
        'pending_approvals': pending_approvals
    })

def delete_patient(request, patient_id):

    patient = get_object_or_404(Patient, id=patient_id)

    
    with transaction.atomic():
        
        if hasattr(patient, 'user'):  
            username = patient.user.username  
            patient.user.delete()
        else:
            username = None

        
        patient.delete()


    if username:
        messages.success(request, f"Patient '{username}' deleted successfully.")
    else:
        messages.success(request, "Patient deleted successfully.")

    return redirect('view_patients')  
def view_doctors(request):
    
    doctors = doctor.objects.select_related('user').filter(user__status=1)  

    
    pending_doctor_approvals = doctor.objects.filter(user__status=0).count()


    pending_approvals = Appointment.objects.filter(status="Pending").count()

    
    return render(request, 'dltdoctor.html', {
        'doctors': doctors,
        'pending_doctor_approvals': pending_doctor_approvals,
        'pending_approvals': pending_approvals
    })

def delete_doctor(request, doctor_id):
    """Delete a specific doctor and the associated CustomUser record."""
    doctorr = get_object_or_404(doctor, id=doctor_id)

    
    with transaction.atomic():
    
        if hasattr(doctorr, 'user'):  
            username = doctorr.user.username  
            doctorr.user.delete()
        else:
            username = None

    
        doctorr.delete()

    
    if username:
        messages.success(request, f"Doctor  '{username}' deleted successfully.")
    else:
        messages.success(request, "Doctor deleted successfully.")

    return redirect('view_doctors')  

def reset(request):
    return render(request, 'resetpatient.html')



def reset_password(request):
    if not request.user.is_authenticated:
    
        messages.error(request, 'You must be logged in to reset your password.')
        return redirect('loginpage') 

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

    
        user = CustomUser.objects.get(id=request.user.id)


        if not check_password(current_password, user.password):  
            messages.error(request, 'Current password is incorrect.')
            return redirect('reset')

        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset')

        
        if len(new_password) < 6 or not any(char.isupper() for char in new_password) \
                or not any(char.isdigit() for char in new_password) \
                or not any(char in '!@#$%^&*()-_+=[]{}|:;"<>,.?/' for char in new_password):
            messages.error(
                request,
                'Password must be at least 6 characters long and contain at least one uppercase letter, one digit, and one special character.'
            )
            return redirect('reset')

    
        user.set_password(new_password)
        user.save()

        messages.success(request, 'Password changed successfully.please login ')
        return redirect('loginpage')  

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    appointment = Appointment.objects.filter(patient=patient).first()  
    doctor = appointment.doctor if appointment else None
    doctor_name = f"{doctor.user.first_name} {doctor.user.last_name}" if doctor else "N/A"
    department_name = doctor.Department.DepatmentName if doctor and doctor.Department else "No Department"
    doctor_image = doctor.Image.url if doctor and doctor.Image else "https://via.placeholder.com/150"
    
    
    return render(request, 'patientcard.html', {'patient': patient,'doctor_name': doctor_name,
        'department_name': department_name,'doctor_image': doctor_image,})
def view_doctor(request):

    approved_doctors = doctor.objects.select_related('user', 'Department').filter(user__status=1)

    return render(request, 'viewdoctor.html', {
        'doctors': approved_doctors,  
    })
def about(request):
    return render(request,'about.html')
def doctoreditpage(request):
    current_user = request.user.id 
    doctor_profile = doctor.objects.get(user_id=current_user)

    

    
    if request.method == 'POST':
    
        doctor_profile.Address = request.POST['address']
        doctor_profile.Contact = request.POST['phone']
        doctor_profile.Age = request.POST['age']


        
        if request.FILES.get('image'):  
            doctor_profile.Image = request.FILES['image']

        
        doctor_profile.save()

    
        messages.success(request, 'Your profile has been updated successfully.')

    
        return redirect('doctoreditpage')  

    else:
        
        context = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'username': request.user.username,
            'email': request.user.email,
            'phone_number': doctor_profile.Contact,
            'address': doctor_profile.Address,
            'age':doctor_profile.Age,
            'department_name': doctor_profile.Department.DepatmentName if doctor_profile.Department else "N/A",
            
            'doctor_image': doctor_profile.Image.url if doctor_profile.Image else None
        }

        return render(request, 'updatedoctor.html', context)
from django.contrib.auth.models import User 
def update_profile(request):
    if request.method == 'POST':
        user = request.user

        
        try:
            doctor_profile = doctor.objects.get(user=user)  
        except doctor.DoesNotExist:
            doctor_profile = None

    
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phone_regex = r'^\d{10}$'  

        if email and not re.match(email_regex, email):
            messages.error(request, "Invalid email format. Please enter a valid email address.")
            return redirect('doctoreditpage')

        if phone and not re.match(phone_regex, phone):
            messages.error(request, "Invalid phone number format. Please enter a 10-digit phone number.")
            return redirect('doctoreditpage')

    
        if email and email != user.email:  
            if CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
                messages.error(request, "The email address is already taken by another user.")
                return redirect('doctoreditpage')

        
        username = request.POST.get('username')
        if username and username != user.username: 
            if CustomUser.objects.filter(username=username).exclude(id=user.id).exists():
                messages.error(request, "The username is already taken by another user.")
                return redirect('doctoreditpage')

    
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = email
        user.username = username
        user.save()

        
        if doctor_profile:
            doctor_profile.Address = request.POST.get('address', doctor_profile.Address)
            doctor_profile.Contact = phone or doctor_profile.Contact
            doctor_profile.Age = request.POST.get('age', doctor_profile.Age)

            
            if 'image' in request.FILES:
                doctor_profile.Image = request.FILES['image']

            doctor_profile.save()

        
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('doctor_profile_view')  

        else:
            messages.error(request, "Doctor profile not found.")
            return redirect('homepage')  

    else:
        
        user = request.user
        try:
            doctor_profile = doctor.objects.get(user=user)  
        except doctor.DoesNotExist:
            doctor_profile = None

        context = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'phone_number': doctor_profile.Contact if doctor_profile else '',
            'address': doctor_profile.Address if doctor_profile else '',
            'age': doctor_profile.Age if doctor_profile else '',
            'doctor_image': doctor_profile.Image.url if doctor_profile and doctor_profile.Image else None
        }

        return render(request, 'updatedoctor.html', context)

def addnewpatient(request):
    if request.method == "POST":
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        username = request.POST.get('username')  
        user_type = request.POST.get('text')  
        age = request.POST.get('age')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        contact = request.POST.get('phone')
        profile_picture = request.FILES.get('profile-picture')

        
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phone_regex = r'^\d{10}$'  

        if email and not re.match(email_regex, email):
            messages.error(request, "Invalid email format. Please enter a valid email address.")
            return redirect('addpatient') 

        if contact and not re.match(phone_regex, contact):
            messages.error(request, "Invalid phone number format. Please enter a 10-digit phone number.")
            return redirect('addpatient')  

    
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different email address.")
            return redirect('addpatient') 

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('addpatient')  

    
        password = generate_password()

    
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,  
            user_type=user_type
        )
        user.save()

        
        random_string = generate_random_string()
        patient_id = f"{username}{random_string}"

        
        patient = Patient.objects.create(
            user=user,
            age=age,
            address=address,
            Gender=gender,
            contact=contact,
            image=profile_picture,
            patient_id=patient_id
        )
        patient.save()

    
        subject = "Patient Registration Details"
        message = (
            f"Dear {first_name} {last_name},\n\n"
            f"Your registration is successful!\n"
            f"Username: {username}\n"
            f"Patient ID: {patient_id}\n"
            f"Password: {password}\n\n"
            f"Please log in to your account."
        )
        recipient_list = [email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

        messages.success(request, "Patient registered successfully! An email has been sent with login credentials.")
        return redirect('addpatient')

    return redirect('adminhome')
@login_required

def doctor_profile_view(request):
    try:
        
        doctor_instance = doctor.objects.get(user=request.user)

        
        department_name = doctor_instance.Department.DepatmentName if doctor_instance.Department else "No Department"

        
        total_pending_appointments = Appointment.objects.filter(
            doctor_id=doctor_instance.id,
            consulted=0,  
            status="Approved"  
        ).count()

        context = {
            'doctor_image': doctor_instance.Image.url if doctor_instance.Image else 'default_image_url',
            'first_name': doctor_instance.user.first_name,
            'last_name': doctor_instance.user.last_name,
            'username': doctor_instance.user.username,
            'department_name': department_name,  
            'doctor_email': doctor_instance.user.email,
            'doctor_contact': doctor_instance.Contact,
            'doctor_address': doctor_instance.Address,
            'doctor_experience': doctor_instance.Age,  
            'total_pending_appointments': total_pending_appointments,  
        }

        return render(request, 'doctorprofile.html', context)

    except doctor.DoesNotExist:
     
        messages.error(request, "Doctor profile not found.")
        return redirect('homepage')  
   
    






def repassword(request):
    if not request.user.is_authenticated:

        messages.error(request, 'You must be logged in to reset your password.')
        return redirect('loginpage')  

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('retype_password')


        user = CustomUser.objects.get(id=request.user.id)

        
        if not check_password(current_password, user.password):  
            messages.error(request, 'Current password is incorrect.')
            return redirect('rsetdoc')

    
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('rsetdoc')

        
        if len(new_password) < 6 or not any(char.isupper() for char in new_password) \
                or not any(char.isdigit() for char in new_password) \
                or not any(char in '!@#$%^&*()-_+=[]{}|:;"<>,.?/' for char in new_password):
            messages.error(
                request,
                'Password must be at least 6 characters long and contain at least one uppercase letter, one digit, and one special character.'
            )
            return redirect('rsetdoc')

    
        user.set_password(new_password)
        user.save()

        messages.success(request, 'Password changed successfully.please login ')
        return redirect('loginpage')  


def rsetdoc(request):
    try:
        
        doctor_instance = doctor.objects.get(user=request.user)

        
        department_name = doctor_instance.Department.DepatmentName

        context = {
            'doctor_image': doctor_instance.Image.url if doctor_instance.Image else 'default_image_url',
            'first_name': doctor_instance.user.first_name,
            'last_name': doctor_instance.user.last_name,
            'department_name': department_name,
        }
    except doctor.DoesNotExist:
    
        messages.error(request, "Doctor profile not found.")
        return redirect('homepage')  

    return render(request, 'resetdoc.html', context)


def display_edit_page(request):
    
    patient = get_object_or_404(Patient, user=request.user)

    return render(request, 'updatepatint.html', {
        'patient': patient  
    })
def edit_profile(request):
    try:
        
        patient = get_object_or_404(Patient, user=request.user)
    except Patient.DoesNotExist:
        messages.error(request, "Patient profile not found.", extra_tags='danger')
        return redirect('homepage')  

    if request.method == 'POST':
    
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        contact = request.POST.get('contact')
        image = request.FILES.get('image')
        email = request.POST.get('email')
        username = request.POST.get('username')

        
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phone_regex = r'^\d{10}$'  

        
        if email and not re.match(email_regex, email):
            messages.error(request, "Invalid email format. Please enter a valid email address.", extra_tags='danger')
            return redirect('display_edit_page')

    
        if contact and not re.match(phone_regex, contact):
            messages.error(request, "Invalid phone number format. Please enter a 10-digit phone number.", extra_tags='danger')
            return redirect('display_edit_page')
        
        if email and email != request.user.email:  
            if CustomUser.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.error(request, "The email address is already taken by another user.", extra_tags='danger')
                return redirect('display_edit_page')  

        
        if username and username != request.user.username: 
            if CustomUser.objects.filter(username=username).exclude(id=request.user.id).exists():
                messages.error(request, "The username is already taken by another user.", extra_tags='danger')
                return redirect('display_edit_page')  

    
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.username = username
        request.user.save()

    
        patient.address = address
        patient.age = age
        patient.Gender = gender
        patient.contact = contact

        if image:  
            patient.image = image

        
        patient.save()

        messages.success(request, "Profile updated successfully.", extra_tags='success')
        return redirect('patieprofile')  

    
    context = {
        'patients': patient
    }
    return render(request, 'updatepatient.html', context)


def consulted_patients_view(request):
    
    consulted_appointments = Appointment.objects.filter(consulted=True).select_related(
        'patient__user', 'doctor__user', 'department'
    )

    
    pending_doctor_approvals = doctor.objects.filter(user__status=0).count()

    
    pending_approvals = Appointment.objects.filter(status="Pending").count()

    
    return render(request, 'consultpdtil.html', {
        'consulted_appointments': consulted_appointments,
        'pending_doctor_approvals': pending_doctor_approvals,
        'pending_approvals': pending_approvals
    })


def togglconsulted(request, appointment_id):


    appointment = get_object_or_404(Appointment, id=appointment_id)

    
    if 'consulted' in request.POST:
        appointment.consulted = 1  
        messages.success(request, "Appointment marked as Consulted.")
    elif 'not_consulted' in request.POST:
        appointment.consulted = 2  
        messages.success(request, "Appointment marked as Not Consulted.")

    
    appointment.save()

    return redirect('instantappointments')
def instantappointments(request):
    try:
    
        doctor_instance = doctor.objects.get(user=request.user)
        

        doctor_image = doctor_instance.Image.url if doctor_instance.Image else None
        first_name = doctor_instance.user.first_name
        last_name = doctor_instance.user.last_name
        department_name = doctor_instance.Department.DepatmentName if doctor_instance.Department else "No Department"
    
    except doctor.DoesNotExist:
    
        messages.error(request, "Doctor profile not found.")
        return redirect("home")

    
    today = timezone.now().date()
    
    
    pending_appointments = Appointment.objects.filter(
        doctor=doctor_instance, 
        status="Approved",  
        appointment_date=today,  
    )
    
    
    return render(request, 'instantapoinmt.html', {
        'appointments': pending_appointments,
        'doctor_image': doctor_image,
        'first_name': first_name,
        'last_name': last_name,
        'department_name': department_name,
        'today': today,  
    })

def display_departments(request):
    departments = depatment.objects.all()  

    
    pending_doctor_approvals = doctor.objects.filter(user__status=0).count()


    pending_approvals = Appointment.objects.filter(status="Pending").count()

    return render(request, 'departmentview.html', {
        'departments': departments,
        'pending_doctor_approvals': pending_doctor_approvals,
        'pending_approvals': pending_approvals
    })

def delete_department(request, department_id):
    department = get_object_or_404(depatment, id=department_id)
    department_name = department.DepatmentName  
    department.delete()
    messages.success(request, f"The department '{department_name}' has been successfully deleted.")
    return redirect('display_departments')
def patieprofile(request):
    
    patient = Patient.objects.filter(user=request.user).first()

    if patient:
        context = {
            'patient': patient
        }
    else:
        context = {
            'error': 'No patient data found for this user.'
        }

    return render(request, 'patientprofile.html', context)
