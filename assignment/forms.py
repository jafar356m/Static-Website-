from django import forms
from django.db.models import fields
from .models import *

class AssignmentForm(forms.ModelForm):
    class Meta:
        model=Assignment
        fields="__all__"

class AssignmentSubmitForm(forms.ModelForm):
    class Meta:
        model=AssignmentSubmit
        fields="__all__"