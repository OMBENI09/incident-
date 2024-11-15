from django import forms
from .models import Incident, Comment

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['title', 'description', 'severity', 'assigned_team', 'image', 'status']  # Removed 'date_reported'
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),  # Optional: for image file input
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
