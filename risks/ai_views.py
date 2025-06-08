from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from .models import Risk, Project
from .ai_features import (
    enhance_risk_description, 
    analyze_risk_trend, 
    generate_risk_response_suggestions,
    smart_risk_search
)

@require_POST
@login_required
def enhance_risk_description_view(request):
    """API endpoint to enhance risk descriptions using Gemini"""
    try:
        data = json.loads(request.body)
        description = data.get('description', '')
        category = data.get('category', None)
        
        if not description:
            return JsonResponse({'error': 'No description provided'}, status=400)
        
        result = enhance_risk_description(description, category)
        
        return JsonResponse({
            'success': True,
            'enhanced_description': result.get('enhanced_description', description),
            'improvements': result.get('improvements', []),
            'sentiment': result.get('sentiment', 'neutral'),
            'clarity_score': result.get('clarity_score', 5)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def analyze_risk_trends_view(request, project_id):
    """Analyze trends across project risks"""
    project = get_object_or_404(Project, id=project_id)
    
    # Get all active risks for the project
    risks = project.risks.filter(status='Open')
    
    if not risks:
        return JsonResponse({
            'success': False,
            'message': 'No active risks found for analysis'
        })
    
    # Extract risk data
    risk_titles = [risk.title for risk in risks]
    risk_descriptions = [risk.description for risk in risks]
    
    # Get the analysis
    analysis = analyze_risk_trend(risk_titles, risk_descriptions)
    
    # Return the results
    return JsonResponse({
        'success': True,
        'project_name': project.name,
        'analysis': analysis,
        'risk_count': len(risk_titles)
    })

@login_required
def generate_risk_response_suggestions_view(request, risk_id):
    """Generate AI-powered risk response suggestions"""
    risk = get_object_or_404(Risk, id=risk_id)
    
    # Convert likelihood and impact to integer values (1, 2, 3)
    likelihood = risk.likelihood
    impact = risk.impact
    
    # Get category name
    category = risk.category.name if risk.category else "General"
    
    # Generate suggestions
    suggestions = generate_risk_response_suggestions(
        risk.description,
        category,
        likelihood,
        impact
    )
    
    return JsonResponse({
        'success': True,
        'risk_title': risk.title,
        'suggestions': suggestions
    })

@require_POST
@login_required
def smart_risk_search_view(request):
    """Natural language search for risks using Gemini"""
    try:
        data = json.loads(request.body)
        query = data.get('query', '')
        project_id = data.get('project_id', None)
        
        if not query:
            return JsonResponse({'error': 'No search query provided'}, status=400)
        
        # Get project context if provided
        project_context = None
        if project_id:
            project = get_object_or_404(Project, id=project_id)
            project_context = f"Project: {project.name} - {project.description}"
        
        # Process the search
        search_result = smart_risk_search(query, project_context)
        
        return JsonResponse({
            'success': True,
            'search_result': search_result,
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
