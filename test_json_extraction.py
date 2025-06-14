#!/usr/bin/env python
"""
Test the fixed extract_json_from_response function
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'risk_manager.settings')
django.setup()

from risks.ai_features import extract_json_from_response
import json

def test_json_extraction():
    """Test the JSON extraction function"""
    
    # Sample response with markdown code blocks
    sample_response = """```json
{
  "identified_patterns": [
    {
      "pattern": "Poor Scope Management",
      "description": "Test description"
    }
  ],
  "mitigation_recommendations": [],
  "potential_blind_spots": []
}
```"""
    
    print("=== Testing JSON Extraction ===")
    print("Original response:")
    print(repr(sample_response))
    
    # Extract JSON
    clean_json = extract_json_from_response(sample_response)
    print("\nExtracted JSON:")
    print(repr(clean_json))
    
    # Try to parse
    try:
        result = json.loads(clean_json)
        print("\n✅ JSON parsing successful!")
        print(f"Keys: {list(result.keys())}")
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON parsing failed: {e}")

if __name__ == "__main__":
    test_json_extraction()
