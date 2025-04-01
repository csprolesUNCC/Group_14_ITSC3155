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
    title = models.CharField("DEFAULT TITLE", max_length=250)
    isbn = models.CharField("-------------", max_length=13)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
