from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['textbook_name', 'college', 'course', 'class_name', 'condition', 'teacher', 'image']
        widgets = {
            'condition': forms.Select(attrs={'class': 'form-select'}),
        }