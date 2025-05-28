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
        fields = ['title', 'description', 'category', 'likelihood', 'impact', 'owner', 'status',
                 'likelihood_percentage', 'optimistic_cost_impact', 'most_likely_cost_impact', 'pessimistic_cost_impact']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'likelihood': forms.Select(attrs={'class': 'form-select'}),
            'impact': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'likelihood_percentage': forms.NumberInput(attrs={'min': 1, 'max': 100, 'step': 1}),
            'optimistic_cost_impact': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'most_likely_cost_impact': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'pessimistic_cost_impact': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        optimistic = cleaned_data.get('optimistic_cost_impact')
        most_likely = cleaned_data.get('most_likely_cost_impact')
        pessimistic = cleaned_data.get('pessimistic_cost_impact')
        
        if optimistic and most_likely and pessimistic:
            if not (optimistic <= most_likely <= pessimistic):
                raise forms.ValidationError(
                    "Cost impacts must be in order: Optimistic ≤ Most Likely ≤ Pessimistic"
                )
        
        return cleaned_data

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
        fields = ['title', 'description', 'category', 'likelihood', 'impact', 'owner', 'status',
                 'likelihood_percentage', 'optimistic_cost_impact', 'most_likely_cost_impact', 'pessimistic_cost_impact']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'likelihood': forms.Select(attrs={'class': 'form-select'}),
            'impact': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'likelihood_percentage': forms.NumberInput(attrs={'min': 1, 'max': 100, 'step': 1}),
            'optimistic_cost_impact': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'most_likely_cost_impact': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'pessimistic_cost_impact': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        optimistic = cleaned_data.get('optimistic_cost_impact')
        most_likely = cleaned_data.get('most_likely_cost_impact')
        pessimistic = cleaned_data.get('pessimistic_cost_impact')
        
        if optimistic and most_likely and pessimistic:
            if not (optimistic <= most_likely <= pessimistic):
                raise forms.ValidationError(
                    "Cost impacts must be in order: Optimistic ≤ Most Likely ≤ Pessimistic"
                )
        
        return cleaned_data