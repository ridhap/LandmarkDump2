from django.db import models

# Create your models here.
class LoginTable(models.Model):
    name= models.CharField(max_length=200, null=True)
    email= models.CharField(max_length=200, null=True)
    phone= models.CharField(max_length=12,null=True)
    date= models.DateTimeField(auto_now_add=True,null=True)