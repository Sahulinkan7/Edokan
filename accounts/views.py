from django.shortcuts import render,redirect
from .forms import SignupForm,LoginForm
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            username=email.split('@')[0]
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()
            print("user created")
            form=SignupForm()
            messages.success(request,f"{username} your account has been created ! ")
    else:
        form=SignupForm()
    context={
        'form':form,
    }
    return render(request,"accounts/registration.html",context)


def login_view(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            form=LoginForm(request.POST)
            if form.is_valid():
                email=request.POST['email']
                password=request.POST['password']
                user=authenticate(email=email,password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request,"Invalid credentials")
        else:
            form=LoginForm()
        context={
            'loginform':form,
        }
        return render(request,"accounts/login.html",context)
    else:
        return redirect("home")

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request,f"You are logged-out from your account ")
    return redirect("login")