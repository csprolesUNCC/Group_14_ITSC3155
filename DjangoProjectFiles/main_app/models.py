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
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    isbn = models.CharField("-------------", max_length=13, null=True)
    description = models.CharField("DEFAULT DESCRIPTION", max_length=512, null=True)
    
class Message(models.Model):
    # maybe change up later 
    # to keep messages between 
    # users even if a user is deleted
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    msg = models.CharField(default="DEFAULT", max_length=255)
    time_sent = models.DateTimeField(auto_now_add=True)