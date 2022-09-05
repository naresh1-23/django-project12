from django.shortcuts import render, redirect
from .models import News
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from news.models import userpayment, Userquery
from users.models import User

def adminhome(request):
    if not request.user.is_superuser:
        messages.error(request,f'access denied')
        return redirect('home')
    user = User.objects.all().count()
    news = News.objects.all().count()
    return render(request, 'adminpage/home.html', {'user': user, 'news':news})
# Create your views here.
@login_required
def UploadPost(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['description']
            image = request.FILES.get('image')
            if title == '' or description == '' or image =='':
                messages.error(request, f'Fields cannot be empty')
            else:
                post = News.objects.create(title = title, description = description, image = image)
                post.save()
                messages.success(request, f'successfully submitted')
                return redirect('admin-uploadpost')
    else:
        messages.error(request, f'Access denied')
        return redirect('home')
    return render(request, 'adminpage/UploadPost.html')

def Viewcomment(request):
    comments = Userquery.objects.all()
    if not request.user.is_superuser:
        messages.error(request, f'Access denied')
        return redirect('home')
    return render(request, 'adminpage/Viewcomment.html', {'comments':comments})

def ViewPaymentDetail(request):
    payments = userpayment.objects.all()
    if not request.user.is_superuser:
        messages.error(request, f'Access denied')
        return redirect('home')
    return render(request, 'adminpage/ViewPaymentDetail.html', {'payments': payments})

def singlepayment(request, id):
    payment_id = id
    payment = userpayment.objects.get(pk = payment_id)
    if not request.user.is_superuser:
        messages.error(request, f'Access denied')
        return redirect('home')
    return render(request, 'adminpage/singlepayment.html', {'payment': payment})
