from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Risk, RiskHistory

def send_high_risk_notification(risk):
    """Send notification when a high risk is created"""
    if not settings.RISK_NOTIFY_HIGH_RISKS:
        return
    
    # Get all managers and admins
    admin_emails = User.objects.filter(
        profile__role__in=['manager', 'admin']
    ).values_list('email', flat=True)
    
    # Filter out empty emails
    admin_emails = [email for email in admin_emails if email]
    
    if not admin_emails:
        return
    
    subject = f'[ALERT] New High Risk: {risk.title}'
    message = f'''
    A new high risk has been identified:
    
    Title: {risk.title}
    Project: {risk.project.name}
    Risk Score: {risk.risk_score}
    Likelihood: {risk.get_likelihood_display()}
    Impact: {risk.get_impact_display()}
    Owner: {risk.owner}
    
    Please review this risk at your earliest convenience.
    '''
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com',
        admin_emails,
        fail_silently=True,
    )

def send_risk_status_change_notification(risk, old_status=None):
    """Send notification when a risk's status changes"""
    if not settings.RISK_NOTIFY_STATUS_CHANGE or not old_status:
        return
    
    # If no actual status change, do nothing
    if risk.status == old_status:
        return
    
    # Determine who should be notified
    notify_emails = []
    
    # Always notify managers and admins
    admin_emails = User.objects.filter(
        profile__role__in=['manager', 'admin']
    ).values_list('email', flat=True)
    notify_emails.extend(admin_emails)
    
    # Filter out empty emails
    notify_emails = [email for email in notify_emails if email]
    
    if not notify_emails:
        return
    
    subject = f'[Update] Risk Status Changed: {risk.title}'
    message = f'''
    A risk's status has been updated:
    
    Title: {risk.title}
    Project: {risk.project.name}
    Old Status: {old_status}
    New Status: {risk.status}
    Risk Score: {risk.risk_score}
    
    Please review this change at your earliest convenience.
    '''
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com',
        notify_emails,
        fail_silently=True,
    )

def send_weekly_summary():
    """Send a weekly summary of risks"""
    # Get all managers and admins
    admin_emails = User.objects.filter(
        profile__role__in=['manager', 'admin']
    ).values_list('email', flat=True)
    
    # Filter out empty emails
    admin_emails = [email for email in admin_emails if email]
    
    if not admin_emails:
        return
    
    # Count risks by level
    from django.db.models import Count
    
    risks = Risk.objects.all()
    high_risks = sum(1 for risk in risks if risk.risk_level == 'High')
    medium_risks = sum(1 for risk in risks if risk.risk_level == 'Medium')
    low_risks = sum(1 for risk in risks if risk.risk_level == 'Low')
    
    # Risk status counts
    open_risks = risks.filter(status='Open').count()
    mitigated_risks = risks.filter(status='Mitigated').count()
    closed_risks = risks.filter(status='Closed').count()
    
    subject = '[Weekly Report] Risk Management Summary'
    message = f'''
    Weekly Risk Management Summary:
    
    Total Risks: {len(risks)}
    
    By Severity:
    - High Risks: {high_risks}
    - Medium Risks: {medium_risks}
    - Low Risks: {low_risks}
    
    By Status:
    - Open: {open_risks}
    - Mitigated: {mitigated_risks}
    - Closed: {closed_risks}
    
    Please login to the system to view detailed reports.
    '''
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com',
        admin_emails,
        fail_silently=True,
    )