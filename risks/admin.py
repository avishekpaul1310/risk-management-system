from django.contrib import admin
from .models import Project, Risk, Category, RiskHistory, RiskResponse, UserProfile

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

@admin.register(RiskHistory)
class RiskHistoryAdmin(admin.ModelAdmin):
    list_display = ('risk', 'changed_at', 'changed_by', 'status', 'likelihood', 'impact')
    list_filter = ('status', 'likelihood', 'impact')
    search_fields = ('risk__title', 'change_comment')
    readonly_fields = ('risk', 'title', 'description', 'category_name', 
                      'likelihood', 'impact', 'status', 'owner', 'changed_by', 'changed_at')

@admin.register(RiskResponse)
class RiskResponseAdmin(admin.ModelAdmin):
    list_display = ('risk', 'response_type', 'status', 'responsible_person', 'target_date', 'created_by')
    list_filter = ('response_type', 'status')
    search_fields = ('risk__title', 'description', 'responsible_person')
    date_hierarchy = 'created_at'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'get_projects')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
    filter_horizontal = ('projects',)
    
    def get_projects(self, obj):
        return ", ".join([p.name for p in obj.projects.all()[:3]])
    get_projects.short_description = "Projects"