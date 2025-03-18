from django import forms
from .models import Project, Risk, Category

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class RiskForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = ['title', 'description', 'category', 'likelihood', 'impact', 'owner', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'likelihood': forms.Select(attrs={'class': 'form-select'}),
            'impact': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }