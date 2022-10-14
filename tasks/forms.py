from django import forms
from .models import Task

class CrearTaks(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Task Description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'})
        }