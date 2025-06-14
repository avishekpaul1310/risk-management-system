from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Project, Risk, Category, RiskHistory, RiskResponse, UserProfile
from .forms import (ProjectForm, RiskForm, CategoryForm, RiskHistoryForm, 
                    RiskResponseForm, UserProfileForm, RiskEditForm)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from .notifications import send_high_risk_notification, send_risk_status_change_notification
from django.urls import reverse
from .monte_carlo import run_monte_carlo_simulation, format_currency
import json

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
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Check if the user has the permissions to delete the project
    try:
        user_profile = request.user.profile
        is_manager = user_profile.is_manager
    except:
        # If user doesn't have a profile yet, create one with limited permissions
        UserProfile.objects.create(user=request.user, role='contributor')
        is_manager = False
    
    if not is_manager:
        messages.error(request, "You don't have permission to delete projects.")
        return redirect('project_detail', project_id=project.id)
    
    if request.method == 'POST':
        project_name = project.name
        project.delete()
        messages.success(request, f'Project "{project_name}" deleted successfully!')
        return redirect('home')
    
    return render(request, 'risks/delete_project.html', {'project': project})

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
            risk.save()
            
            # Create initial history record
            history = RiskHistory(
                risk=risk,
                title=risk.title,
                description=risk.description,
                category_name=risk.category.name if risk.category else '',
                likelihood=risk.likelihood,
                impact=risk.impact,
                status=risk.status,
                owner=risk.owner,
                changed_by=request.user,
                change_comment="Initial risk creation"
            )
            history.save()
            
            # Send notification for high risks
            if risk.risk_level == 'High':
                send_high_risk_notification(risk)
                
            messages.success(request, f'Risk "{risk.title}" added successfully!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = RiskForm()
    return render(request, 'risks/add_risk.html', {'form': form, 'project': project})

@login_required
def edit_risk(request, risk_id):
    risk = get_object_or_404(Risk, id=risk_id)
    old_status = risk.status
    old_category_name = risk.category.name if risk.category else ''
    
    if request.method == 'POST':
        form = RiskEditForm(request.POST, instance=risk)
        if form.is_valid():
            # Save the risk with its updated values
            updated_risk = form.save()
            
            # Create a history record
            history = RiskHistory(
                risk=risk,
                title=risk.title,
                description=risk.description,
                category_name=risk.category.name if risk.category else '',
                likelihood=risk.likelihood,
                impact=risk.impact,
                status=risk.status,
                owner=risk.owner,
                changed_by=request.user,
                change_comment=form.cleaned_data.get('change_comment', '')
            )
            history.save()
            
            # Send notification if status changed
            if risk.status != old_status:
                send_risk_status_change_notification(risk, old_status)
                
            messages.success(request, f'Risk "{risk.title}" updated successfully!')
            return redirect('project_detail', project_id=risk.project.id)
    else:
        form = RiskEditForm(instance=risk)
    
    # Get risk history for display
    risk_history = risk.history.all()
    
    return render(request, 'risks/edit_risk.html', {
        'form': form, 
        'risk': risk,
        'history': risk_history
    })

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
    open_risks_queryset = risks.filter(status='Open')
    
    # Project statistics
    project_count = projects.count()
    
    # Risk statistics (all risks)
    risk_count = risks.count()
    
    # Calculate risk levels based on Open risks only (for dashboard focus)
    high_risks = sum(1 for risk in open_risks_queryset if risk.risk_level == 'High')
    medium_risks = sum(1 for risk in open_risks_queryset if risk.risk_level == 'Medium')
    low_risks = sum(1 for risk in open_risks_queryset if risk.risk_level == 'Low')
      # Risks by status
    open_risks = open_risks_queryset.count()
    mitigated_risks = risks.filter(status='Mitigated').count()
    closed_risks = risks.filter(status='Closed').count()
    
    # Risks by category (Open risks only for dashboard focus)
    categories = Category.objects.all()
    risks_by_category = {}
    for category in categories:
        count = open_risks_queryset.filter(category=category).count()
        if count > 0:  # Only include categories that have open risks
            risks_by_category[category.name] = count    # Recent risks (last 10) - focus on recent Open risks for dashboard relevance
    recent_risks = open_risks_queryset.order_by('-created_at')[:10]
    
    # All risks with pagination - ordered by risk score (likelihood * impact) descending
    all_risks_queryset = risks.order_by('-likelihood', '-impact', 'title')
    
    # Handle pagination for all risks
    page = request.GET.get('page', 1)
    paginator = Paginator(all_risks_queryset, 20)  # Show 20 risks per page
    
    try:
        all_risks_page = paginator.page(page)
    except PageNotAnInteger:
        all_risks_page = paginator.page(1)
    except EmptyPage:
        all_risks_page = paginator.page(paginator.num_pages)
    
    # Prepare data for risk matrix (heat map) - use only Open risks for active risk management
    risk_matrix = [
        [0, 0, 0],  # Low likelihood: [low impact, med impact, high impact]
        [0, 0, 0],  # Med likelihood: [low impact, med impact, high impact]
        [0, 0, 0],  # High likelihood: [low impact, med impact, high impact]
    ]
    
    # Count risks for each cell in the matrix (Open risks only)
    for risk in open_risks_queryset:
        if risk.likelihood > 0 and risk.impact > 0:  # Ensure valid values
            li = risk.likelihood - 1  # 0-based index (likelihood is 1, 2, or 3)
            im = risk.impact - 1      # 0-based index (impact is 1, 2, or 3)
            if 0 <= li < 3 and 0 <= im < 3:  # Ensure within valid range
                risk_matrix[li][im] += 1
    
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
    
    status_data = {
        'labels': ['Open', 'Mitigated', 'Closed'],
        'values': [open_risks, mitigated_risks, closed_risks]
    }
    
    # Convert risk matrix to the format expected by Chart.js matrix plugin
    risk_matrix_data = []
    for x in range(3):  # Likelihood (0=Low, 1=Medium, 2=High)
        for y in range(3):  # Impact (0=Low, 1=Medium, 2=High)
            # Calculate risk score (likelihood+1 * impact+1)
            score = (x + 1) * (y + 1)
            count = risk_matrix[x][y]
            risk_matrix_data.append({
                'x': x,
                'y': y,
                'v': score,
                'count': count
            })    
    context = {
        'projects': projects,
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
        'all_risks_page': all_risks_page,
        'severity_data': severity_data,
        'category_data': category_data,
        'status_data': status_data,
        'risk_matrix_data': risk_matrix_data,
        # Add project-specific risk data for modals
        'projects_with_risk_data': [
            {
                'project': project,
                'total_risks': project.risks.count(),
                'open_risks': project.risks.filter(status='Open').count(),
                'high_risks': sum(1 for risk in project.risks.all() if risk.risk_level == 'High'),
                'medium_risks': sum(1 for risk in project.risks.all() if risk.risk_level == 'Medium'),
                'low_risks': sum(1 for risk in project.risks.all() if risk.risk_level == 'Low'),
            }
            for project in projects
        ]
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

@login_required
def risk_detail(request, risk_id):
    """View for detailed risk information including history and responses"""
    risk = get_object_or_404(Risk, id=risk_id)
    history = risk.history.all()
    responses = risk.responses.all().order_by('-updated_at')
    
    context = {
        'risk': risk,
        'history': history,
        'responses': responses,
    }
    return render(request, 'risks/risk_detail.html', context)

@login_required
def add_risk_response(request, risk_id):
    """Add a new response to a risk, optionally using AI suggestions"""
    risk = get_object_or_404(Risk, id=risk_id)
    
    if request.method == 'POST':
        form = RiskResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.risk = risk
            response.created_by = request.user
            response.save()
            
            messages.success(request, f'Response added successfully to risk "{risk.title}"')
            return redirect('risk_detail', risk_id=risk.id)
    else:
        # Check for AI suggested responses from query parameters
        suggested_response = request.GET.get('suggested_response', '')
        suggested_type = request.GET.get('suggested_type', '')
          # Initialize form with suggested values if provided
        initial_data = {}
        if suggested_response:
            initial_data['description'] = suggested_response
        if suggested_type:
            # Map AI suggestion type to form choices
            type_mapping = {
                'Avoid': 'Avoid',
                'Transfer': 'Transfer',
                'Mitigate': 'Mitigate',
                'Accept': 'Accept'
            }
            mapped_type = type_mapping.get(suggested_type, '')
            if mapped_type:
                initial_data['response_type'] = mapped_type
        
        form = RiskResponseForm(initial=initial_data)
    
    return render(request, 'risks/add_risk_response.html', {
        'form': form,
        'risk': risk,
        'is_ai_suggested': bool(request.GET.get('suggested_response'))
    })

@login_required
def edit_risk_response(request, response_id):
    """Edit an existing risk response"""
    response = get_object_or_404(RiskResponse, id=response_id)
    risk = response.risk
    
    # Check if the user has permission to edit the response
    try:
        user_profile = request.user.profile
        is_contributor = user_profile.is_contributor
    except:
        # If user doesn't have a profile yet, create one
        UserProfile.objects.create(user=request.user, role='contributor')
        is_contributor = True
    
    if not is_contributor and response.created_by != request.user:
        messages.error(request, "You don't have permission to edit this response.")
        return redirect('risk_detail', risk_id=risk.id)
    
    if request.method == 'POST':
        form = RiskResponseForm(request.POST, instance=response)
        if form.is_valid():
            form.save()
            messages.success(request, 'Response updated successfully')
            return redirect('risk_detail', risk_id=risk.id)
    else:
        form = RiskResponseForm(instance=response)
    
    return render(request, 'risks/edit_risk_response.html', {
        'form': form,
        'response': response,
        'risk': risk
    })

@login_required
def delete_risk_response(request, response_id):
    """Delete a risk response"""
    response = get_object_or_404(RiskResponse, id=response_id)
    risk = response.risk
    
    # Check if the user has permission to delete the response
    try:
        user_profile = request.user.profile
        is_manager = user_profile.is_manager
    except:
        # If user doesn't have a profile yet, create one
        UserProfile.objects.create(user=request.user, role='contributor')
        is_manager = False
    
    if not is_manager and response.created_by != request.user:
        messages.error(request, "You don't have permission to delete this response.")
        return redirect('risk_detail', risk_id=risk.id)
    
    if request.method == 'POST':
        response.delete()
        messages.success(request, 'Response deleted successfully')
        return redirect('risk_detail', risk_id=risk.id)
    
    return render(request, 'risks/delete_risk_response.html', {
        'response': response,
        'risk': risk
    })

@login_required
def edit_user_profile(request):
    """Edit the current user's profile"""
    user_profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'risks/edit_profile.html', {'form': form})

@login_required
def monte_carlo_simulation(request, project_id):
    """Run Monte Carlo simulation for project risk costs"""
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        # Get number of simulations from request (default to 5000)
        num_simulations = int(request.POST.get('num_simulations', 5000))
        
        # Validate simulation count
        if num_simulations < 100:
            num_simulations = 100
        elif num_simulations > 10000:
            num_simulations = 10000
        
        # Run the simulation
        results = run_monte_carlo_simulation(project.risks, num_simulations)
        
        # Format results for display
        formatted_stats = {}
        for key, value in results['statistics'].items():
            formatted_stats[key] = format_currency(value)
        
        # Return JSON response for AJAX
        return JsonResponse({
            'success': True,
            'results': results,
            'formatted_stats': formatted_stats,
            'project_name': project.name
        })
    
    # For GET request, show the simulation page
    active_risks = project.risks.filter(status='Open')
    return render(request, 'risks/monte_carlo_simulation.html', {
        'project': project,
        'active_risks': active_risks,
        'total_active_risks': active_risks.count()
    })