from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .models import User
from .tokens import account_activation_token
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin


class changepassword(SuccessMessageMixin,PasswordChangeView):
    from_class = PasswordChangeForm
    success_message = "password changes successfully"
    success_url = reverse_lazy('home')

    
def activateEmail(request, user, to_email):
    mail_subject = 'Activate Your user account'
    message = render_to_string(
        "users/activate_template.html",{
            'user': user,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user.username}, please go to your email {to_email} inbox and clock on\
            recieved activation link to confirm and complete the registration. \nNote:  Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email} , check if you typed it correctly. ')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    except:
        user = None
    if user is not None and  account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()

        messages.success(request, f'Now your email is verified.')
        return redirect('login')
    else:
        messages.error(request, 'activation link is invalid')
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        if email == '' or username == '' or password == '':
            messages.error(request, f'Fields cannot be empty')
        elif User.objects.filter(email = email).exists():
            messages.error(request, f'Email already exists')
        elif User.objects.filter(username = username).exists():
            messages.error(request, f'Username already taken')
        else:
            user = User.objects.create_user(username = username, email = email, password = password)
            user.is_verified = False
            user.save()
            activateEmail(request, user, email)
            messages.success(request, f'Your account has been created.')
            return redirect('login')
    return render(request, 'users/SignUp.html')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if username == '' or password == '':
            messages.error(request, f'Fields cannot be empty')
        elif user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('admin-home')
            elif user.is_verified == False:
                user.delete()
                messages.error(request, f'Account doesnt exist. Please register your account')
                return redirect('register')
            else:
                login(request, user)
                return redirect('user-admin')
        else:
            messages.error(request, f'Username or password is incorrect')
    return render(request, 'users/Login.html')



@login_required
def logout_views(request):
    logout(request)
    return redirect('home')
