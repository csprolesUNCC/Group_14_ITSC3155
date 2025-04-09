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
    description = models.CharField("DEFAULT DESCRIPTION", max_length=512)
    

CONDITION_CHOICES = [
    ('new', 'New'),
    ('like_new', 'Like New'),
    ('good', 'Good'),
    ('acceptable', 'Acceptable'),
    ('poor', 'Poor'),
]

class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    textbook_name = models.CharField(max_length=200)
    college = models.CharField(max_length=200)
    course = models.CharField(max_length=100)
    class_name = models.CharField(max_length=200)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    teacher = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='listing_images/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.textbook_name
