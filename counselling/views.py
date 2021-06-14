from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.
from accounts.models import College
from .models import Request, Schedule
from .forms import ScheduleForm, RequestForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

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
        return render(request, "index.html", {"colleges": colleges})

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
        schedules = Schedule.objects.filter(counselor=request.user, date__gte=timezone.now())
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
    return render(request, "pages/my_requests.html", {"pending_requests":pending_requests, "my_requests":my_requests})
