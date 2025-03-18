from django.contrib import admin
from .models import Project, Risk, Category

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'category', 'risk_score', 'risk_level', 'status', 'owner')
    list_filter = ('category', 'status', 'likelihood', 'impact')
    search_fields = ('title', 'description', 'owner')
    list_editable = ('status', 'owner')