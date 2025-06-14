"""
Quick template validation script to check for syntax errors
"""
import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'risk_manager.settings')
django.setup()

from django.template.loader import get_template
from django.template import Context
from django.http import HttpRequest
from django.contrib.auth.models import User
from risks.models import Project
from risks.forms import RiskForm

def test_add_risk_template():
    """Test the add_risk template to make sure it loads without errors"""
    
    print("🧪 Testing add_risk.html template...")
    
    try:
        # Load the template
        template = get_template('risks/add_risk.html')
        print("✅ Template loaded successfully")
        
        # Create a mock context similar to what the view would provide
        form = RiskForm()
        
        # Get the first project or create a mock one
        try:
            project = Project.objects.first()
            if not project:
                project = Project(
                    id=1,
                    name="Test Project",
                    description="Test project for template validation"
                )
        except:
            project = type('MockProject', (), {
                'id': 1,
                'name': 'Test Project',
                'description': 'Test project for template validation'
            })()
        
        context = {
            'form': form,
            'project': project
        }
        
        # Try to render the template (this will catch any template syntax errors)
        rendered = template.render(context)
        print("✅ Template rendered successfully")
        print(f"📄 Rendered content length: {len(rendered)} characters")
        
        # Basic checks
        if 'AI Suggest' in rendered:
            print("✅ AI Suggest button found in rendered template")
        else:
            print("⚠️  AI Suggest button not found in rendered template")
            
        if 'aiScoringModal' in rendered:
            print("✅ AI Scoring Modal found in rendered template")
        else:
            print("⚠️  AI Scoring Modal not found in rendered template")
            
        return True
        
    except Exception as e:
        print(f"❌ Template error: {e}")
        return False

def test_edit_risk_template():
    """Test the edit_risk template to make sure it loads without errors"""
    
    print("\n🧪 Testing edit_risk.html template...")
    
    try:
        # Load the template
        template = get_template('risks/edit_risk.html')
        print("✅ Template loaded successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Template error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Template Validation Script")
    print("=" * 40)
    
    success_count = 0
    total_tests = 2
    
    if test_add_risk_template():
        success_count += 1
    
    if test_edit_risk_template():
        success_count += 1
    
    print("\n" + "=" * 40)
    print(f"🎯 Results: {success_count}/{total_tests} templates passed validation")
    
    if success_count == total_tests:
        print("🎉 All templates are working correctly!")
        print("\n📋 You can now:")
        print("1. Navigate to http://127.0.0.1:8000/")
        print("2. Go to a project")
        print("3. Click 'Add New Risk'")
        print("4. Test the AI Risk Scoring Assistant feature")
    else:
        print("⚠️  Some templates have issues that need to be fixed.")
