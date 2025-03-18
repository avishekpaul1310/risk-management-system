from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Project, Risk, Category
from .forms import ProjectForm, RiskForm, CategoryForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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