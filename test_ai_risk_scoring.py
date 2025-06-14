"""
Test script for AI Risk Scoring Assistant

This script tests the AI Risk Scoring Assistant functionality to ensure it works correctly
with the Gemini-1.5-Flash integration.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'risk_manager.settings')
django.setup()

from risks.ai_features import ai_risk_scoring_assistant

def test_ai_risk_scoring():
    """Test the AI Risk Scoring Assistant with sample data"""
    
    print("🤖 Testing AI Risk Scoring Assistant")
    print("=" * 50)
    
    # Test case 1: Technical Risk
    print("\n📋 Test Case 1: Technical Risk")
    test_risk_1 = {
        'title': 'Database Performance Degradation',
        'description': 'The main database server is showing signs of performance degradation under high load. Query response times have increased by 40% over the past month, and we\'re approaching peak usage periods.',
        'category': 'Technical',
        'project_context': 'E-commerce platform upgrade project with expected 3x traffic increase during holiday season'
    }
    
    try:
        result_1 = ai_risk_scoring_assistant(
            risk_title=test_risk_1['title'],
            risk_description=test_risk_1['description'],
            risk_category=test_risk_1['category'],
            project_context=test_risk_1['project_context']
        )
        
        print(f"✅ AI Analysis Complete")
        print(f"   Likelihood: {result_1['suggested_likelihood']['score']} ({result_1['suggested_likelihood']['percentage_range']})")
        print(f"   Impact: {result_1['suggested_impact']['score']} ({result_1['suggested_impact']['severity_level']})")
        print(f"   Risk Level: {result_1['overall_risk_assessment']['risk_level']}")
        print(f"   Priority: {result_1['overall_risk_assessment']['priority_ranking']}")
        print(f"   Confidence: {result_1['confidence_level']}")
        
    except Exception as e:
        print(f"❌ Error in Test Case 1: {str(e)}")
    
    # Test case 2: Financial Risk
    print("\n📋 Test Case 2: Financial Risk")
    test_risk_2 = {
        'title': 'Budget Overrun Due to Scope Creep',
        'description': 'Client is requesting additional features that were not in the original scope. The development team estimates an additional 200 hours of work, which would exceed our allocated budget by 25%.',
        'category': 'Financial',
        'project_context': 'Fixed-price contract for custom software development with strict budget constraints'
    }
    
    try:
        result_2 = ai_risk_scoring_assistant(
            risk_title=test_risk_2['title'],
            risk_description=test_risk_2['description'],
            risk_category=test_risk_2['category'],
            project_context=test_risk_2['project_context']
        )
        
        print(f"✅ AI Analysis Complete")
        print(f"   Likelihood: {result_2['suggested_likelihood']['score']} ({result_2['suggested_likelihood']['percentage_range']})")
        print(f"   Impact: {result_2['suggested_impact']['score']} ({result_2['suggested_impact']['severity_level']})")
        print(f"   Risk Level: {result_2['overall_risk_assessment']['risk_level']}")
        print(f"   Priority: {result_2['overall_risk_assessment']['priority_ranking']}")
        print(f"   Confidence: {result_2['confidence_level']}")
        
        # Show detailed analysis for this test case
        print(f"\n📊 Detailed Analysis:")
        print(f"   Likelihood Reasoning: {result_2['suggested_likelihood']['reasoning'][:100]}...")
        print(f"   Impact Reasoning: {result_2['suggested_impact']['reasoning'][:100]}...")
        print(f"   Key Factors: {', '.join(result_2['suggested_likelihood']['key_factors'][:3])}")
        print(f"   Affected Areas: {', '.join(result_2['suggested_impact']['affected_areas'][:3])}")
        
    except Exception as e:
        print(f"❌ Error in Test Case 2: {str(e)}")
    
    # Test case 3: Minimal Input (Edge Case)
    print("\n📋 Test Case 3: Minimal Input")
    test_risk_3 = {
        'title': 'Team Member Availability',
        'description': 'Key developer may not be available during critical project phase.',
        'category': None,
        'project_context': None
    }
    
    try:
        result_3 = ai_risk_scoring_assistant(
            risk_title=test_risk_3['title'],
            risk_description=test_risk_3['description'],
            risk_category=test_risk_3['category'],
            project_context=test_risk_3['project_context']
        )
        
        print(f"✅ AI Analysis Complete (Minimal Input)")
        print(f"   Likelihood: {result_3['suggested_likelihood']['score']}")
        print(f"   Impact: {result_3['suggested_impact']['score']}")
        print(f"   Confidence: {result_3['confidence_level']}")
        
    except Exception as e:
        print(f"❌ Error in Test Case 3: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 AI Risk Scoring Assistant Test Complete!")
    print("\nNext Steps:")
    print("1. Run the Django development server")
    print("2. Navigate to a project and click 'Add New Risk'")
    print("3. Fill in risk title and description")
    print("4. Click the 'AI Suggest' button to test the feature")
    print("\nCommand to start server:")
    print("python manage.py runserver")

if __name__ == "__main__":
    test_ai_risk_scoring()
