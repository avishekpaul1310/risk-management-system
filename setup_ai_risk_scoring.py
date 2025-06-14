"""
Setup script for AI Risk Scoring Assistant

This script helps configure the AI Risk Scoring Assistant feature in your Risk Management System.
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if all required packages are installed"""
    print("🔍 Checking Requirements...")
    
    required_packages = [
        'google-generativeai',
        'django',
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package} is installed")
        except ImportError:
            print(f"   ❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("   ✅ All packages installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Error installing packages: {e}")
            return False
    
    return True

def check_api_key():
    """Check if Gemini API key is configured"""
    print("\n🔑 Checking API Configuration...")
    
    # Try to read from Django settings
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'risk_manager.settings')
        django.setup()
        
        from django.conf import settings
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        
        if api_key:
            if api_key.startswith('AIza') and len(api_key) > 30:
                print("   ✅ GEMINI_API_KEY is configured in Django settings")
                return True
            else:
                print("   ⚠️  GEMINI_API_KEY format looks incorrect")
        else:
            print("   ❌ GEMINI_API_KEY not found in Django settings")
    except Exception as e:
        print(f"   ❌ Error checking Django settings: {e}")
    
    # Check environment variables
    env_api_key = os.getenv('GEMINI_API_KEY')
    if env_api_key:
        print("   ✅ GEMINI_API_KEY found in environment variables")
        return True
    
    print("\n📝 To configure your Gemini API key:")
    print("   1. Get your API key from: https://aistudio.google.com/app/apikey")
    print("   2. Add it to your Django settings.py:")
    print("      GEMINI_API_KEY = 'your-api-key-here'")
    print("   3. Or set it as an environment variable:")
    print("      set GEMINI_API_KEY=your-api-key-here  (Windows)")
    print("      export GEMINI_API_KEY=your-api-key-here  (Linux/Mac)")
    
    return False

def check_database():
    """Check if database migrations are up to date"""
    print("\n🗄️  Checking Database...")
    
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'risk_manager.settings')
        django.setup()
        
        from django.core.management import execute_from_command_line
        
        # Check for unapplied migrations
        print("   Running migration check...")
        try:
            execute_from_command_line(['manage.py', 'migrate', '--check'])
            print("   ✅ Database is up to date")
            return True
        except SystemExit as e:
            if e.code != 0:
                print("   ⚠️  Unapplied migrations found")
                print("   Running migrations...")
                try:
                    execute_from_command_line(['manage.py', 'migrate'])
                    print("   ✅ Migrations applied successfully")
                    return True
                except SystemExit:
                    print("   ❌ Error applying migrations")
                    return False
    except Exception as e:
        print(f"   ❌ Error checking database: {e}")
        return False

def check_static_files():
    """Check if static files are properly configured"""
    print("\n📁 Checking Static Files...")
    
    static_dirs = [
        'risks/static/risks/js',
        'staticfiles'
    ]
    
    for static_dir in static_dirs:
        if os.path.exists(static_dir):
            print(f"   ✅ {static_dir} exists")
        else:
            print(f"   ⚠️  {static_dir} not found")
    
    # Check if ai_features.js exists (it should be created by the system)
    ai_js_path = 'risks/static/risks/js/ai_features.js'
    if os.path.exists(ai_js_path):
        print("   ✅ AI features JavaScript file found")
    else:
        print("   ℹ️  AI features JavaScript file will be created automatically")
    
    return True

def run_test():
    """Run a basic test of the AI functionality"""
    print("\n🧪 Running Basic Test...")
    
    try:
        # Import and test the AI function
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'risk_manager.settings')
        django.setup()
        
        from risks.ai_features import ai_risk_scoring_assistant
        
        # Simple test
        result = ai_risk_scoring_assistant(
            risk_title="Test Risk",
            risk_description="This is a test risk to verify the AI functionality is working correctly.",
            risk_category="Technical"
        )
        
        if result and 'suggested_likelihood' in result:
            print("   ✅ AI Risk Scoring Assistant is working!")
            print(f"   Sample result: Likelihood {result['suggested_likelihood']['score']}, Impact {result['suggested_impact']['score']}")
            return True
        else:
            print("   ❌ AI returned unexpected result format")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing AI functionality: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 AI Risk Scoring Assistant Setup")
    print("=" * 50)
    
    # Run all checks
    checks = [
        ("Requirements", check_requirements),
        ("API Key", check_api_key),
        ("Database", check_database),
        ("Static Files", check_static_files),
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        if not check_func():
            all_passed = False
    
    # Run test if all checks pass
    if all_passed:
        print("\n🎯 All checks passed! Running functionality test...")
        if run_test():
            print("\n🎉 Setup Complete!")
            print("\nThe AI Risk Scoring Assistant is ready to use!")
            print("\nTo use the feature:")
            print("1. Start the Django server: python manage.py runserver")
            print("2. Navigate to a project")
            print("3. Click 'Add New Risk' or edit an existing risk")
            print("4. Fill in the risk title and description")
            print("5. Click the 'AI Suggest' button")
        else:
            print("\n⚠️  Setup incomplete - AI test failed")
    else:
        print("\n⚠️  Setup incomplete - please fix the issues above")
    
    print("\n📚 For more information, see:")
    print("   - AI_RISK_SCORING_GUIDE.md")
    print("   - AI_FEATURES_GUIDE.md")
    print("   - USER_MANUAL.md")

if __name__ == "__main__":
    main()
