from django.shortcuts import render,redirect,HttpResponse
from .forms import SignupForm,LoginForm
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required

# verification librarires
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage,send_mail
from django.conf import settings
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
            
            # user activation
            
            current_site=get_current_site(request)
            mail_subject="Please activate your account"
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            
            form=SignupForm()
            messages.success(request,f" Account activation link has been sent. Please check !")
            return redirect("login")
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
                    guestuser=Account.objects.get(email=email)
                    if guestuser.is_active==False:
                        messages.error(request,"You are not verified. Please verify first")
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

def activate_view(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
        
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congratulations , your account is activated')
        return redirect('login')
    else:
        messages.error(request,"Invalid activation link")
        return redirect("register")
    
def dashboard_view(request):
    return render(request,"accounts/dashboard.html")

def forgotPassword_view(request):
    if request.method=='POST':
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)
            
            # send forgot password link
            current_site=get_current_site(request)
            mail_subject="Password reset Link"
            message = render_to_string('accounts/reset_password_validate_email.html',{
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,"password reset mail has been sent")
            return redirect("login")
            
        else:
            messages.error(request,"Account does not exist !")
            return redirect("forgotPassword")
    return render(request,"accounts/forgotPassword.html")

def resetPassword_validate_view(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'please reset your password')
        return redirect('resetpassword') 
    else:
        messages.error(request,"This link has been expired !")
        return redirect("login")
    
def resetPassword_view(request):
    if request.method=='POST':
        password=request.POST['password']
        conf_password=request.POST['conf_password']
        
        if password==conf_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,"password reset successfull !")
            return redirect("login")
        else:
            messages.error(request,"password do not match")
            return redirect("resetpassword")
    return render(request,"accounts/resetPassword.html")