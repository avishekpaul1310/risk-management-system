from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('project/add/', views.add_project, name='add_project'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('project/<int:project_id>/add_risk/', views.add_risk, name='add_risk'),
    path('risk/<int:risk_id>/edit/', views.edit_risk, name='edit_risk'),
    path('risk/<int:risk_id>/delete/', views.delete_risk, name='delete_risk'),
    
    # New category URLs
    path('categories/', views.categories, name='categories'),
    path('category/add/', views.add_category, name='add_category'),
    path('category/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    
    # Authentication URLs
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reports/export-csv/', views.export_risks_csv, name='export_risks_csv'),
]