from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Project, Risk, Category
from .forms import ProjectForm, RiskForm, CategoryForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import csv
from django.http import HttpResponse
from datetime import datetime

# User registration view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'risks/signup.html', {'form': form})

@login_required
def profile(request):
    
    user_risks = Risk.objects.all().order_by('-created_at')
    
    context = {
        'user': request.user,
        'risks': user_risks
    }
    return render(request, 'risks/profile.html', context)

@login_required
def home(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'risks/home.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    # Order by likelihood and impact which together determine the risk score
    risks = project.risks.all().order_by('-likelihood', '-impact', 'title')
    
    # Count risks by level
    high_risks = sum(1 for risk in risks if risk.risk_level == 'High')
    medium_risks = sum(1 for risk in risks if risk.risk_level == 'Medium')
    low_risks = sum(1 for risk in risks if risk.risk_level == 'Low')
    
    # Count risks by status
    open_risks = sum(1 for risk in risks if risk.status == 'Open')
    mitigated_risks = sum(1 for risk in risks if risk.status == 'Mitigated')
    closed_risks = sum(1 for risk in risks if risk.status == 'Closed')
    
    context = {
        'project': project,
        'risks': risks,
        'risk_stats': {
            'total': len(risks),
            'high': high_risks,
            'medium': medium_risks,
            'low': low_risks,
            'open': open_risks,
            'mitigated': mitigated_risks,
            'closed': closed_risks,
        }
    }
    return render(request, 'risks/project_detail.html', context)

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, f'Project "{project.name}" created successfully!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'risks/add_project.html', {'form': form})

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f'Project "{project.name}" updated successfully!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'risks/edit_project.html', {'form': form, 'project': project})

@login_required
def categories(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'risks/categories.html', {'categories': categories})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('categories')
    else:
        form = CategoryForm()
    return render(request, 'risks/add_category.html', {'form': form})

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'risks/edit_category.html', {'form': form, 'category': category})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        # Check if the category is being used
        if Risk.objects.filter(category=category).exists():
            messages.error(request, f'Cannot delete category "{category.name}" because it is used by existing risks.')
            return redirect('categories')
        
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('categories')
    return render(request, 'risks/delete_category.html', {'category': category})

@login_required
def add_risk(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = RiskForm(request.POST)
        if form.is_valid():
            risk = form.save(commit=False)
            risk.project = project
            
            # Add the user if authenticated
            if request.user.is_authenticated:
                risk.created_by = request.user
                
            risk.save()
            messages.success(request, f'Risk "{risk.title}" added successfully!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = RiskForm()
    return render(request, 'risks/add_risk.html', {'form': form, 'project': project})

@login_required
def edit_risk(request, risk_id):
    risk = get_object_or_404(Risk, id=risk_id)
    if request.method == 'POST':
        form = RiskForm(request.POST, instance=risk)
        if form.is_valid():
            form.save()
            messages.success(request, f'Risk "{risk.title}" updated successfully!')
            return redirect('project_detail', project_id=risk.project.id)
    else:
        form = RiskForm(instance=risk)
    return render(request, 'risks/edit_risk.html', {'form': form, 'risk': risk})

@login_required
def delete_risk(request, risk_id):
    risk = get_object_or_404(Risk, id=risk_id)
    project_id = risk.project.id
    risk_title = risk.title
    if request.method == 'POST':
        risk.delete()
        messages.success(request, f'Risk "{risk_title}" deleted successfully!')
        return redirect('project_detail', project_id=project_id)
    return render(request, 'risks/delete_risk.html', {'risk': risk})

@login_required
def dashboard(request):
    # Get all projects and risks
    projects = Project.objects.all()
    risks = Risk.objects.all()
    
    # Project statistics
    project_count = projects.count()
    
    # Risk statistics
    risk_count = risks.count()
    
    # Calculate risk levels based on the risk_level property
    high_risks = sum(1 for risk in risks if risk.risk_level == 'High')
    medium_risks = sum(1 for risk in risks if risk.risk_level == 'Medium')
    low_risks = sum(1 for risk in risks if risk.risk_level == 'Low')
    
    # Risks by status
    open_risks = risks.filter(status='Open').count()
    mitigated_risks = risks.filter(status='Mitigated').count()
    closed_risks = risks.filter(status='Closed').count()
    
    # Risks by category
    categories = Category.objects.all()
    risks_by_category = {}
    for category in categories:
        risks_by_category[category.name] = risks.filter(category=category).count()
    
    # Recent risks (last 10)
    recent_risks = risks.order_by('-created_at')[:10]
    
    # High priority risks
    high_priority_risks = risks.filter(status='Open').order_by('-likelihood', '-impact')[:10]
    
    # Prepare data for JSON serialization
    severity_data = {
        'high': high_risks,
        'medium': medium_risks,
        'low': low_risks
    }
    
    category_data = {
        'labels': list(risks_by_category.keys()),
        'values': list(risks_by_category.values())
    }
    
    context = {
        'project_count': project_count,
        'risk_count': risk_count,
        'high_risks': high_risks,
        'medium_risks': medium_risks,
        'low_risks': low_risks,
        'open_risks': open_risks,
        'mitigated_risks': mitigated_risks,
        'closed_risks': closed_risks,
        'risks_by_category': risks_by_category,
        'recent_risks': recent_risks,
        'high_priority_risks': high_priority_risks,
        'severity_data': severity_data,
        'category_data': category_data
    }
    
    return render(request, 'risks/dashboard.html', context)

@login_required
def export_risks_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="risks_export_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Project', 'Risk Title', 'Description', 'Category', 'Likelihood', 'Impact', 
                    'Risk Score', 'Risk Level', 'Owner', 'Status', 'Created', 'Updated'])
    
    risks = Risk.objects.all().order_by('project__name', '-likelihood', '-impact')
    
    for risk in risks:
        writer.writerow([
            risk.project.name,
            risk.title,
            risk.description,
            risk.category.name if risk.category else '',
            risk.get_likelihood_display(),
            risk.get_impact_display(),
            risk.risk_score,
            risk.risk_level,
            risk.owner,
            risk.status,
            risk.created_at.strftime('%Y-%m-%d'),
            risk.updated_at.strftime('%Y-%m-%d'),
        ])
    
    return response