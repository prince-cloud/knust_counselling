from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from accounts.models import College
from .models import Request, Schedule
from .forms import ScheduleForm, RequestForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from accounts.forms import StudentSignUpForm, SignupForm, CustomUserChangeForm
from accounts.models import Student
from django.contrib.auth import login
from django.db.models import Q 

from django.contrib.auth import get_user_model

User = get_user_model()


def index(request):
    if hasattr(request.user, "student"):
        schedules = Schedule.objects.filter(request__user=request.user, date__gte=timezone.now())

        return render(request, 'pages/student_view.html', {"schedules":schedules})

    elif hasattr(request.user, "counselor"):
        college = request.user.counselor.college
        counselling_requests = Request.objects.filter(
            college=college, viewed=False)
        return render(request, 'pages/counselor_view.html', {"counselling_requests": counselling_requests, })

    else:
        colleges = College.objects.all()
        return render(request, "index.html", {"colleges": colleges, })

@login_required
def counselling_requests(request):
    college = request.user.counselor.college
    counselling_requests = Request.objects.filter(college=college)
    return render(request, 'pages/requests.html', {"counselling_requests": counselling_requests})

@login_required
def view_counselling_request(request, id):
    counselling_request = get_object_or_404(Request, pk=id)
    counselling_request.viewed = True
    counselling_request.save()
    return render(request, 'pages/view_counselling_request.html', {"counselling_request": counselling_request})

@login_required
def schedule_request(request, id):
    counselling_request = get_object_or_404(Request, pk=id)
    if request.method == 'POST':
        form = ScheduleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.counselor = request.user
            appointment_date = form.cleaned_data['date']
            if appointment_date < timezone.now():
                messages.info(
                request, f"Sorry, appointment date, cannot be less than today's date."
                )
                return render(request, "pages/schedule.html", {"form": form})

            schedule.request = counselling_request
            counselling_request.scheduled = True
            counselling_request.viewed = True
            schedule.save()
            counselling_request.save()

            messages.success(
                request, f"Schedule with {counselling_request.user} is completed."
            )
            return redirect(counselling_request.get_requests())

        else:
            messages.info(
                request, "There was an Error in form. Please check and try again."
            )
    else:
        form = ScheduleForm()
    return render(request, "pages/schedule.html", {"form": form})

@login_required
def my_schedules(request):
    if hasattr(request.user, "student"):
        schedules = Schedule.objects.filter(request__user=request.user, date__gte=timezone.now())
        return render(request, 'pages/student_schedules.html', {"schedules":schedules})
        
    else:
        schedules = Schedule.objects.filter(counselor=request.user, date__gte=timezone.now(), deleted=False)
        return render(request, 'pages/my_schedules.html', {"schedules":schedules})

@login_required
def make_request(request):
    if request.method == "POST":
        form = RequestForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            request_form = form.save(commit=False)
            request_form.user = request.user
            request_form.college = request.user.student.college
            request_form.save()
        
            messages.success(
                request, f"Request completed. Your college counselor will schedule meetings with you soon."
            )

            return redirect("/")
        
        else:
            messages.info(
                request, "There was an Error in form. Please check and try again."
            )
    else:
        form = RequestForm()

    return render(request, "pages/make_request.html", {"form":form})

@login_required
def my_requests(request):
    pending_requests = Request.objects.filter(user=request.user, scheduled=False)
    my_requests = Request.objects.filter(user=request.user)
    return render(request, "pages/my_requests.html", 
        {"pending_requests":pending_requests, "my_requests":my_requests}
    )


@login_required
def delete_appointment(request, id):
    appointment = get_object_or_404(Schedule, pk=id)
    appointment.deleted = True
    messages.success(
                request, f"Appointment succesffully deleted"
            )
    return redirect('/')

@login_required
def reschudle_appointment(request, id):
    appointment = get_object_or_404(Schedule, id=id)
    if request.method =='POST':
        form = ScheduleForm(data=request.POST, files=request.FILES, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Appointment reschudelued successfully."
            )
            return redirect('/')
        else:
            messages.warning(
                request, "Error. please check the form and try again."
            )
    else:
        form = ScheduleForm(instance=appointment)
    return render(request, "pages/schedule.html", {"form": form})

def student_signup(request):
    if request.method == 'POST':
        user_form = SignupForm(data=request.POST, files=request.FILES)
        student_form = StudentSignUpForm(data=request.POST, files=request.FILES)
        if student_form.is_valid() and user_form.is_valid():
            user = user_form.save(request)

            student_signup = student_form.save(commit=False)
            student_signup.user = user
            student_signup.save()

            login(
                request, user=user, backend="django.contrib.auth.backends.ModelBackend"
            )
            messages.success(
                request, f"Account succesffuly created."
            )
            
            return redirect("/")
        else:
            messages.warning(
                request, "There was an Error in form. Please check and try again."
            )
    else:
        student_form = StudentSignUpForm()
        user_form = SignupForm()
    return render(request, "account/student_signup.html", {"student_form":student_form, "user_form":user_form})

def view_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if hasattr(user, "student"):
        return render(request, "view_student.html", {"student":"student"})

    elif hasattr(user, "counselor"):
        return render(request, "view_counselor.html", {"counselor":"counselor"})

@login_required
def edit_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_form = CustomUserChangeForm(data=request.POST, files=request.FILES, instance=user)
        student_form = StudentSignUpForm(data=request.POST, files=request.FILES, instance=user.student)
        if student_form.is_valid() and user_form.is_valid():
            user = user_form.save(request)
            user.save()
            #student_signup = student_form.save(commit=False)
            #student_signup.user = user
            student = student_form
            student.save()

            messages.success(
                request, f"Account succesffuly updated"
            )
            
            return redirect("/")
        else:
            messages.warning(
                request, "There was an Error in form. Please check and try again."
            )
    else:
        student_form = StudentSignUpForm(instance=user.student)
        user_form = CustomUserChangeForm(instance=user)
    return render(request, "account/student_signup.html", {"student_form":student_form, "user_form":user_form})

@login_required
def student_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'pages/student_profile.html', {"user":user})

@login_required
def counselor_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'pages/counselor_profile.html', {"user":user})

@login_required
def all_students(request):
    user = request.user

    search = request.GET.get("search")
    filter_type = request.GET.get("filter_type")

    if search and (filter_type=="student_id"):
        students = Student.objects.filter(college=user.counselor.college, student_id = search)
    elif search and (filter_type=="index_number"):
        students = Student.objects.filter(college=user.counselor.college, index_number = search)
    elif search and (filter_type=="name"):
        students = Student.objects.filter(
            Q(user__first_name__icontains=search) | 
            Q(user__last_name__icontains=search), 
            college=user.counselor.college, 
        )
    else:
        students = Student.objects.filter(college=user.counselor.college)
    return render (request, 'pages/all_students.html', {
        "students":students, 
        "search":search, 
        "filter_type":filter_type
        }
    )
