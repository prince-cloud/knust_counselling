from django.shortcuts import render

# Create your views here.
from accounts.forms import StudentSignUpForm
from allauth.account.forms import SignupForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

def student_signup(request):
    if request.method == 'POST':
        user_form = SignupForm(data=request.POST, files=request.FILES)
        student_form = StudentSignUpForm(data=request.POST, files=request.FILES)
        if student_form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_student = True
            user.save()
            
            student_signup = student_form.save(commit=False)
            student_signup.user = user
            student_signup.save()

            messages.success(
                request, f"Account succesffuly created."
            )

            login(
                request, user=user, backend="django.contrib.auth.backends.ModelBackend"
            )
            #return redirect("login")
        else:
            messages.warning(
                request, "There was an Error in form. Please check and try again."
            )
    else:
        student_form = StudentSignUpForm()
        user_form = SignupForm()
    return render(request, "account/student_signup.html", {"student_form":student_form, "user_form":user_form})
    