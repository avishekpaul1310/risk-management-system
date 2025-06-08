from django.urls import path
from . import ai_views, ai_page_views

urlpatterns = [
    # API endpoints for AI features
    path('enhance-risk-description/', ai_views.enhance_risk_description_view, name='enhance_risk_description'),
    path('analyze-risk-trends/<int:project_id>/', ai_views.analyze_risk_trends_view, name='analyze_risk_trends'),
    path('generate-response-suggestions/<int:risk_id>/', ai_views.generate_risk_response_suggestions_view, name='generate_risk_response_suggestions'),
    path('smart-risk-search/', ai_views.smart_risk_search_view, name='smart_risk_search'),
    
    # Page views for AI features
    path('project/<int:project_id>/analysis/', ai_page_views.risk_ai_analysis, name='risk_ai_analysis'),
]
