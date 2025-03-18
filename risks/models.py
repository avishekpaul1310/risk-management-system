from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Risk(models.Model):
    LIKELIHOOD_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    
    IMPACT_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    
    CATEGORY_CHOICES = [
        ('Technical', 'Technical'),
        ('Financial', 'Financial'),
        ('Operational', 'Operational'),
        ('Legal', 'Legal'),
    ]
    
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Mitigated', 'Mitigated'),
        ('Closed', 'Closed'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='risks')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='risks')
    likelihood = models.IntegerField(choices=LIKELIHOOD_CHOICES, default=1)
    impact = models.IntegerField(choices=IMPACT_CHOICES, default=1)
    owner = models.CharField(max_length=100, blank=True)  # Risk Owner
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def risk_score(self):
        return self.likelihood * self.impact
    
    @property
    def risk_level(self):
        score = self.risk_score
        if score >= 6:
            return 'High'
        elif score >= 3:
            return 'Medium'
        else:
            return 'Low'

    def __str__(self):
        return f"{self.title} ({self.project.name})"