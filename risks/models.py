from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

class RiskHistory(models.Model):
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE, related_name='history')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category_name = models.CharField(max_length=100)
    likelihood = models.IntegerField()
    impact = models.IntegerField()
    status = models.CharField(max_length=20)
    owner = models.CharField(max_length=100, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    change_comment = models.TextField(blank=True)

    class Meta:
        ordering = ['-changed_at']
        verbose_name_plural = "Risk histories"

    def __str__(self):
        return f"{self.risk.title} - {self.changed_at.strftime('%Y-%m-%d %H:%M')}"

class RiskResponse(models.Model):
    RESPONSE_TYPES = [
        ('Avoid', 'Avoid'),
        ('Transfer', 'Transfer'),
        ('Mitigate', 'Mitigate'),
        ('Accept', 'Accept'),
    ]
    
    RESPONSE_STATUS = [
        ('Planned', 'Planned'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar ($)'),
        ('GBP', 'British Pound (£)'),
        ('EUR', 'Euro (€)'),
        ('INR', 'Indian Rupee (₹)'),
    ]
    
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE, related_name='responses')
    response_type = models.CharField(max_length=20, choices=RESPONSE_TYPES)
    description = models.TextField()
    cost_estimate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    responsible_person = models.CharField(max_length=100)
    target_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=RESPONSE_STATUS, default='Planned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_responses')

    def __str__(self):
        return f"{self.get_response_type_display()} - {self.risk.title}"
        
    def get_currency_symbol(self):
        currency_symbols = {
            'USD': '$',
            'GBP': '£',
            'EUR': '€',
            'INR': '₹',
        }
        return currency_symbols.get(self.currency, '$')

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('viewer', 'Viewer'),
        ('contributor', 'Contributor'),
        ('manager', 'Manager'),
        ('admin', 'Administrator'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='contributor')
    projects = models.ManyToManyField(Project, blank=True, related_name='team_members')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    @property
    def is_admin(self):
        return self.role == 'admin'
        
    @property
    def is_manager(self):
        return self.role == 'manager' or self.role == 'admin'
    
    @property
    def is_contributor(self):
        return self.role in ['contributor', 'manager', 'admin']

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile for every new User"""
    if created:
        UserProfile.objects.create(user=instance)