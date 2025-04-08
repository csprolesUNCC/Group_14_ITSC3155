from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#
# This is the products model
# Once we get a users model impemented 
# we can uncomment the author member line
#
# for title and ISBN there are default values 
# set up if none we passed in creation.
#
class Product(models.Model):
    title = models.CharField("DEFAULT TITLE", max_length=250, null=False)
    uploader = models.CharField(max_length=150, null=False)
    isbn = models.CharField("-------------", max_length=13, null=True)
    description = models.CharField("DEFAULT DESCRIPTION", max_length=512, null=True)
    
class Chats(models.Model):
    sender = models.CharField(max_length=150, related_name="sender")
    receiver = models.CharField(max_length=150, related_name="receiver")
    body = models.CharField(default="DEFAULT", max_length=255)
    time_sent = models.DateTimeField(auto_now_add=True)