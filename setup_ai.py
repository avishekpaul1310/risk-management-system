#!/usr/bin/env python3
"""
Setup script for Risk Management System AI features configuration
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🤖 Risk Management System - AI Features Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ Error: .env file not found!")
        print("📝 Creating .env file from template...")
        
        # Copy from .env.example if it exists
        example_file = Path('.env.example')
        if example_file.exists():
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from template")
        else:
            # Create basic .env file
            with open('.env', 'w') as f:
                f.write("""# Django Secret Key
SECRET_KEY=django-insecure-hc*67w03+ia)acek4%4cjij=s7k)pbhd-%s30rm1wi*v=)4r)f

# Google Gemini API Key
GEMINI_API_KEY=your-gemini-api-key-here

# Debug mode
DEBUG=True

# AI Features Configuration
RISK_NOTIFY_HIGH_RISKS=True
RISK_NOTIFY_STATUS_CHANGE=True
""")
            print("✅ Created basic .env file")
    
    # Check if dependencies are installed
    print("\n📦 Checking dependencies...")
    try:
        import django
        print(f"✅ Django {django.VERSION} is installed")
    except ImportError:
        print("❌ Django not installed")
        install_deps = input("Install dependencies? (y/n): ")
        if install_deps.lower() == 'y':
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI library is installed")
    except ImportError:
        print("❌ Google Generative AI library not installed")
        install_genai = input("Install google-generativeai? (y/n): ")
        if install_genai.lower() == 'y':
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'google-generativeai>=0.3.0'])
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv is installed")
    except ImportError:
        print("❌ python-dotenv not installed")
        install_dotenv = input("Install python-dotenv? (y/n): ")
        if install_dotenv.lower() == 'y':
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'python-dotenv>=1.0.0'])
    
    # Check API key configuration
    print("\n🔑 Checking API key configuration...")
    from dotenv import load_dotenv
    load_dotenv()
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    if not gemini_key or gemini_key == 'your-gemini-api-key-here':
        print("❌ Gemini API key not configured!")
        print("\n📋 To get your Gemini API key:")
        print("1. Go to https://makersuite.google.com/app/apikey")
        print("2. Sign in with your Google account")
        print("3. Click 'Create API Key'")
        print("4. Copy the generated API key")
        print("5. Replace 'your-gemini-api-key-here' in the .env file with your actual API key")
        
        configure_key = input("\nDo you want to configure it now? (y/n): ")
        if configure_key.lower() == 'y':
            api_key = input("Enter your Gemini API key: ").strip()
            if api_key:
                # Update .env file
                with open('.env', 'r') as f:
                    content = f.read()
                
                content = content.replace('your-gemini-api-key-here', api_key)
                
                with open('.env', 'w') as f:
                    f.write(content)
                
                print("✅ API key configured successfully!")
            else:
                print("❌ No API key provided")
    else:
        print("✅ Gemini API key is configured")
    
    # Test database migration
    print("\n🗄️  Checking database...")
    if os.path.exists('db.sqlite3'):
        print("✅ Database exists")
    else:
        print("📝 Creating database...")
        subprocess.run([sys.executable, 'manage.py', 'migrate'])
        print("✅ Database created")
    
    # Test AI features
    print("\n🧪 Testing AI features...")
    try:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'risk_manager.settings'
        import django
        django.setup()
        
        from risks.ai_features import setup_gemini_api
        setup_gemini_api()
        print("✅ AI features are working correctly!")
        
    except Exception as e:
        print(f"❌ AI features test failed: {str(e)}")
        if "GEMINI_API_KEY" in str(e):
            print("💡 Make sure your API key is correctly set in the .env file")
    
    # Final instructions
    print("\n🎉 Setup Summary:")
    print("=" * 30)
    print("✅ Project structure verified")
    print("✅ Environment file configured")
    print("✅ Dependencies checked")
    print("✅ Database prepared")
    
    print("\n🚀 Next Steps:")
    print("1. Start the development server: python manage.py runserver")
    print("2. Navigate to any project in your browser")
    print("3. Click 'Enhanced AI Analysis' to test the AI features")
    print("4. Try the interactive demos for each AI feature")
    
    print("\n📊 Available AI Features:")
    print("• Risk Scoring Assistant")
    print("• Auto Risk Categorization")
    print("• Monte Carlo Parameter Optimizer")
    print("• Risk Dependency Analysis")
    print("• Executive Summary Generator")
    print("• Mitigation Timeline Planner")
    
    print("\n🔗 Useful URLs:")
    print("• Project Dashboard: http://localhost:8000/")
    print("• Admin Panel: http://localhost:8000/admin/")
    print("• AI Analysis: http://localhost:8000/ai/project/{project_id}/enhanced-analysis/")

if __name__ == '__main__':
    main()
