from django.urls import path
from . import ai_views, ai_page_views

urlpatterns = [
    # API endpoints for existing AI features
    path('enhance-risk-description/', ai_views.enhance_risk_description_view, name='enhance_risk_description'),
    path('analyze-risk-trends/<int:project_id>/', ai_views.analyze_risk_trends_view, name='analyze_risk_trends'),
    path('generate-response-suggestions/<int:risk_id>/', ai_views.generate_risk_response_suggestions_view, name='generate_risk_response_suggestions'),
    path('smart-risk-search/', ai_views.smart_risk_search_view, name='smart_risk_search'),
    
    # API endpoints for new AI features
    path('ai-risk-scoring/', ai_views.ai_risk_scoring_assistant_view, name='ai_risk_scoring'),
    path('auto-categorize-risk/', ai_views.auto_categorize_risk_view, name='auto_categorize_risk'),
    path('optimize-monte-carlo/', ai_views.optimize_monte_carlo_estimates_view, name='optimize_monte_carlo'),
    path('analyze-dependencies/<int:project_id>/', ai_views.analyze_risk_dependencies_view, name='analyze_risk_dependencies'),
    path('executive-summary/<int:project_id>/', ai_views.generate_executive_summary_view, name='generate_executive_summary'),
    path('mitigation-timeline/', ai_views.generate_mitigation_timeline_view, name='generate_mitigation_timeline'),
      # Page views for AI features
    path('project/<int:project_id>/analysis/', ai_page_views.risk_ai_analysis, name='risk_ai_analysis'),
    path('project/<int:project_id>/enhanced-analysis/', ai_page_views.enhanced_ai_analysis, name='enhanced_ai_analysis'),
]
