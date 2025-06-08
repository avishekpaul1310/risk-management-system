from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project

@login_required
def risk_ai_analysis(request, project_id):
    """Display the AI risk analysis page for a project"""
    project = get_object_or_404(Project, id=project_id)
    active_risks = project.risks.filter(status='Open')
    
    context = {
        'project': project,
        'active_risks': active_risks,
        'total_active_risks': active_risks.count()
    }
    
    return render(request, 'risks/risk_ai_analysis.html', context)
