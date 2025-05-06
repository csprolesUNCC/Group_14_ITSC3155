from django import forms
from .models import Listing
from django.forms import modelformset_factory

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['textbook_name', 'price', 'college', 'course', 'class_name', 'condition', 'teacher', 'image']
        widgets = {
            'condition': forms.Select(attrs={'class': 'form-select'}),
        }