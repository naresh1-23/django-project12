from django.shortcuts import render, redirect
from .models import userpayment, Userquery
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from adminpage.models import News

def home(request):
    news = News.objects.all()
    return render(request, 'news/index.html', {'news': news})

@login_required
def useradmin(request):
    user = request.user
    payments = userpayment.objects.filter(author = user)
    if request.method == 'POST':
        name = request.POST['name']
        contact = request.POST['contact']
        location = request.POST['location']
        userimage = request.FILES['userImage']
        paymentimage = request.FILES['paymentImage']
        if name == '' or contact == '' or location =='' or userimage == '' or paymentimage == '':
            messages.error(request, f'Fields cannot be empty')
        elif len(contact)!=10 or contact.isdigit() == False:
            messages.error(request, f'enter valid number')
        else:
            post = userpayment.objects.create(name= name, contact_number = contact, location = location, your_pic = userimage, payment_pic = paymentimage, author = request.user)
            post.save()
            messages.success(request, f'form successfully submitted')
            return redirect('user-admin')
    return render(request, 'news/Useradmin.html', {'payments': payments})

def userquery(request):
    if request.method == 'POST':
        email = request.POST['email']
        query = request.POST['query']
        if email == '' or query == '':
            messages.error(request, f'Fields cannot be empty')
        else:
            queries = Userquery.objects.create(email = email, description = query, author = request.user)
            queries.save()
            messages.success(request, f'Successfully submitted')
            return redirect('home')
    return redirect('home')

def singlepayment(request, id):
    payment_id = id
    payment = userpayment.objects.get(pk = payment_id)
    return render(request, 'news/singlepayment.html', {'payment': payment})