from django import forms
from .models import Project, Risk, Category, RiskResponse, UserProfile, RiskHistory

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

class RiskHistoryForm(forms.ModelForm):
    class Meta:
        model = RiskHistory
        fields = ['change_comment']
        widgets = {
            'change_comment': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Describe what changed and why'}),
        }

class RiskResponseForm(forms.ModelForm):
    class Meta:
        model = RiskResponse
        fields = ['response_type', 'description', 'cost_estimate', 'currency', 'responsible_person', 'target_date', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'response_type': forms.Select(attrs={'class': 'form-select'}),
            'currency': forms.Select(attrs={'class': 'form-select'}),
            'cost_estimate': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'responsible_person': forms.TextInput(),
            'target_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'projects']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
            'projects': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
        }

class RiskEditForm(forms.ModelForm):
    change_comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Describe what changed and why'}),
        required=False
    )
    
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