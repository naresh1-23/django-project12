from distutils.command.upload import upload
from django.db import models
from users.models import User

class userpayment(models.Model):
    name = models.CharField(max_length=300)
    contact_number = models.CharField(max_length=10)
    location = models.CharField(max_length=500)
    your_pic = models.ImageField(upload_to='user_pic/',blank = False)
    payment_pic = models.ImageField(upload_to='payment/',blank = False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Userquery(models.Model):
    email = models.EmailField()
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)