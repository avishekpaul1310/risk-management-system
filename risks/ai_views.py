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
    smart_risk_search,
    ai_risk_scoring_assistant,
    auto_categorize_risk,
    optimize_monte_carlo_estimates,
    analyze_risk_dependencies,
    generate_executive_summary,
    generate_mitigation_timeline
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

@require_POST
@login_required
def ai_risk_scoring_assistant_view(request):
    """AI-powered risk scoring suggestions with reasoning"""
    try:
        data = json.loads(request.body)
        description = data.get('description', '')
        category = data.get('category', None)
        project_id = data.get('project_id', None)
        
        if not description:
            return JsonResponse({'error': 'No risk description provided'}, status=400)
        
        # Get similar risks for context if project is specified
        similar_risks = []
        if project_id:
            project = get_object_or_404(Project, id=project_id)
            # Get similar risks from the same project
            project_risks = project.risks.all()[:5]  # Limit to 5 for context
            similar_risks = [
                {
                    'title': risk.title,
                    'likelihood': risk.likelihood,
                    'impact': risk.impact,
                    'risk_score': risk.risk_score
                }
                for risk in project_risks
            ]
        
        result = ai_risk_scoring_assistant(description, category, similar_risks)
        
        return JsonResponse({
            'success': True,
            'scoring_suggestion': result
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_POST
@login_required
def auto_categorize_risk_view(request):
    """Auto-categorize risk based on description using AI"""
    try:
        data = json.loads(request.body)
        description = data.get('description', '')
        
        if not description:
            return JsonResponse({'error': 'No risk description provided'}, status=400)
        
        # Get available categories from the database
        from .models import Category
        available_categories = list(Category.objects.values_list('name', flat=True))
        
        if not available_categories:
            # Fallback to default categories if none exist in database
            available_categories = ['Technical', 'Financial', 'Operational', 'Legal']
        
        result = auto_categorize_risk(description, available_categories)
        
        return JsonResponse({
            'success': True,
            'categorization': result
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_POST
@login_required
def optimize_monte_carlo_estimates_view(request):
    """AI-powered Monte Carlo parameter optimization"""
    try:
        data = json.loads(request.body)
        description = data.get('description', '')
        category = data.get('category', None)
        project_id = data.get('project_id', None)
        
        if not description:
            return JsonResponse({'error': 'No risk description provided'}, status=400)
        
        # Get historical cost data for context if project is specified
        historical_data = []
        if project_id:
            project = get_object_or_404(Project, id=project_id)
            # Get historical cost data from similar risks
            project_risks = project.risks.exclude(
                most_likely_cost_impact=0
            ).values(
                'title', 'description', 'most_likely_cost_impact', 'category__name'
            )[:5]
            
            historical_data = [
                {
                    'description': risk['title'],
                    'cost': float(risk['most_likely_cost_impact']),
                    'category': risk['category__name']
                }
                for risk in project_risks
            ]
        
        result = optimize_monte_carlo_estimates(description, category, historical_data)
        
        return JsonResponse({
            'success': True,
            'monte_carlo_suggestions': result
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def analyze_risk_dependencies_view(request, project_id):
    """Analyze risk dependencies and cascade effects for a project"""
    try:
        project = get_object_or_404(Project, id=project_id)
        
        # Get all risks for the project
        risks = project.risks.all()
        
        if not risks:
            return JsonResponse({
                'success': False,
                'message': 'No risks found for dependency analysis'
            })
        
        # Prepare risk data for analysis
        project_risks = []
        for risk in risks:
            project_risks.append({
                'title': risk.title,
                'description': risk.description,
                'category': risk.category.name if risk.category else 'N/A',
                'risk_score': risk.risk_score,
                'likelihood': risk.likelihood,
                'impact': risk.impact,
                'status': risk.status
            })
        
        result = analyze_risk_dependencies(project_risks)
        
        return JsonResponse({
            'success': True,
            'project_name': project.name,
            'dependency_analysis': result,
            'total_risks_analyzed': len(project_risks)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def generate_executive_summary_view(request, project_id):
    """Generate executive summary for project risks"""
    try:
        project = get_object_or_404(Project, id=project_id)
        
        # Get all risks for the project
        risks = project.risks.all()
        
        if not risks:
            return JsonResponse({
                'success': False,
                'message': 'No risks found for executive summary'
            })
        
        # Prepare risk data
        project_risks = []
        for risk in risks:
            project_risks.append({
                'title': risk.title,
                'description': risk.description,
                'category': risk.category.name if risk.category else 'N/A',
                'risk_score': risk.risk_score,
                'likelihood': risk.likelihood,
                'impact': risk.impact,
                'status': risk.status,
                'most_likely_cost': float(risk.most_likely_cost_impact) if risk.most_likely_cost_impact else 0
            })
        
        # Calculate basic Monte Carlo context (simplified)
        monte_carlo_results = None
        total_exposure = sum([risk['most_likely_cost'] for risk in project_risks])
        if total_exposure > 0:
            monte_carlo_results = {
                'expected_value': total_exposure,
                'percentile_95': total_exposure * 1.5  # Simplified calculation
            }
        
        result = generate_executive_summary(project_risks, monte_carlo_results)
        
        return JsonResponse({
            'success': True,
            'project_name': project.name,
            'executive_summary': result,
            'total_risks': len(project_risks),
            'total_financial_exposure': total_exposure
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_POST
@login_required
def generate_mitigation_timeline_view(request):
    """Generate optimal timeline for risk mitigation activities"""
    try:
        data = json.loads(request.body)
        project_id = data.get('project_id')
        constraints = data.get('constraints', {})
        
        if not project_id:
            return JsonResponse({'error': 'Project ID required'}, status=400)
        
        project = get_object_or_404(Project, id=project_id)
        
        # Get risk responses - for now we'll simulate based on existing risks
        # In a full implementation, you'd have a RiskResponse model
        risks = project.risks.filter(status='Open')
        
        if not risks:
            return JsonResponse({
                'success': False,
                'message': 'No open risks found for timeline generation'
            })
        
        # Create simulated risk responses based on existing risks
        risk_responses = []
        for risk in risks:
            # Generate a basic response for each risk
            risk_responses.append({
                'strategy': f"Mitigate {risk.title}",
                'risk_title': risk.title,
                'type': 'Mitigate',
                'implementation_complexity': 'Medium' if risk.risk_score >= 6 else 'Low',
                'estimated_effectiveness': 70 if risk.risk_score >= 6 else 50,
                'resources_required': f"Team effort for {risk.category.name if risk.category else 'general'} risk"
            })
        
        result = generate_mitigation_timeline(risk_responses, constraints)
        
        return JsonResponse({
            'success': True,
            'project_name': project.name,
            'mitigation_timeline': result,
            'total_responses': len(risk_responses)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
