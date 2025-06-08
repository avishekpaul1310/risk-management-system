"""
AI-powered features for the Risk Management System using Google's Gemini 1.5 Flash
"""
import os
import json
from typing import Dict, List, Any, Optional, Tuple
import google.generativeai as genai
from django.conf import settings

# Configure the Gemini API
def setup_gemini_api():
    """Initialize the Gemini API with the API key from settings"""
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in settings")
    genai.configure(api_key=api_key)

def enhance_risk_description(raw_description: str, category: str = None) -> Dict[str, Any]:
    """
    Use Gemini to enhance and standardize risk descriptions.
    
    Args:
        raw_description: The original risk description from the user
        category: Optional risk category to provide context
        
    Returns:
        Dictionary with enhanced description and suggested improvements
    """
    setup_gemini_api()
    
    # Create a system prompt with formatting instructions
    context = f"Category: {category}" if category else "No category specified"
    
    # Initialize the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Create the prompt with guidance for the model
    prompt = f"""
    As a risk management expert, improve this risk description to be clearer and more specific.
    
    CONTEXT:
    {context}
    
    ORIGINAL RISK DESCRIPTION:
    {raw_description}
    
    INSTRUCTIONS:
    1. Enhance the description to be more specific and actionable
    2. Use standard risk management terminology
    3. Make sure it clearly explains the risk's nature and potential consequences
    4. Keep it concise (max 3-4 sentences)
    5. Return the enhanced description and a list of improvements made
    
    FORMAT YOUR RESPONSE AS JSON:
    {{
      "enhanced_description": "The improved risk description",
      "improvements": ["Improvement 1", "Improvement 2", ...],
      "sentiment": "positive/negative/neutral",
      "clarity_score": 1-10
    }}
    """
    
    try:
        # Generate the response
        response = model.generate_content(prompt)
        
        # Parse the JSON response
        result = json.loads(response.text)
        return result
    
    except Exception as e:
        # Fallback if API call fails
        print(f"Error enhancing risk description: {e}")
        return {
            "enhanced_description": raw_description,
            "improvements": ["AI enhancement unavailable"],
            "sentiment": "neutral",
            "clarity_score": 5
        }

def analyze_risk_trend(risk_titles: List[str], risk_descriptions: List[str]) -> Dict[str, Any]:
    """
    Analyze trends across multiple project risks to identify common themes or patterns.
    
    Args:
        risk_titles: List of risk titles
        risk_descriptions: List of risk descriptions
        
    Returns:
        Dictionary with identified patterns and recommendations
    """
    setup_gemini_api()
    
    # Prepare input data - combine titles and descriptions
    risks_data = []
    for i, (title, desc) in enumerate(zip(risk_titles, risk_descriptions)):
        risks_data.append(f"Risk {i+1}: {title} - {desc}")
    
    risks_text = "\n\n".join(risks_data)
    
    # Initialize the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Create the prompt
    prompt = f"""
    As a risk management consultant, analyze these project risks to identify patterns and provide recommendations.
    
    PROJECT RISKS:
    {risks_text}
    
    INSTRUCTIONS:
    1. Identify the top 3-5 common themes or patterns
    2. Suggest risk mitigation strategies
    3. Highlight any potential blind spots
    4. Return your analysis as structured JSON
    
    FORMAT YOUR RESPONSE AS JSON:
    {{
      "identified_patterns": [
        {{
          "pattern": "Pattern name",
          "description": "Pattern description",
          "affected_risks": [risk numbers]
        }}
      ],
      "mitigation_recommendations": [
        {{
          "recommendation": "Specific recommendation",
          "addresses_patterns": [pattern names]
        }}
      ],
      "potential_blind_spots": [
        "Blind spot description"
      ]
    }}
    """
    
    try:
        # Generate the response
        response = model.generate_content(prompt)
        
        # Parse the JSON response
        result = json.loads(response.text)
        return result
    
    except Exception as e:
        # Fallback if API call fails
        print(f"Error analyzing risk trends: {e}")
        return {
            "identified_patterns": [],
            "mitigation_recommendations": [],
            "potential_blind_spots": ["AI analysis unavailable"]
        }

def generate_risk_response_suggestions(risk_description: str, risk_category: str, 
                                      likelihood: int, impact: int) -> List[Dict[str, str]]:
    """
    Generate tailored risk response suggestions based on the risk details.
    
    Args:
        risk_description: Description of the risk
        risk_category: Category of the risk (Technical, Financial, etc.)
        likelihood: Risk likelihood (1=Low, 2=Medium, 3=High)
        impact: Risk impact (1=Low, 2=Medium, 3=High)
        
    Returns:
        List of response strategy dictionaries
    """
    setup_gemini_api()
    
    # Map numeric values to text representations
    likelihood_text = {1: "Low", 2: "Medium", 3: "High"}.get(likelihood, "Medium")
    impact_text = {1: "Low", 2: "Medium", 3: "High"}.get(impact, "Medium")
    
    # Initialize the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Create the prompt
    prompt = f"""
    As a risk management consultant, suggest response strategies for this risk.
    
    RISK DETAILS:
    Description: {risk_description}
    Category: {risk_category}
    Likelihood: {likelihood_text}
    Impact: {impact_text}
    
    INSTRUCTIONS:
    1. Suggest 3 risk response strategies from these categories: Avoid, Transfer, Mitigate, Accept
    2. For each strategy, provide a specific action plan
    3. Include estimated effectiveness (percentage)
    4. Include implementation complexity (Low, Medium, High)
    5. Return a structured JSON array of 3 suggested responses
    
    FORMAT YOUR RESPONSE AS JSON:
    [
      {{
        "strategy": "Strategy name",
        "type": "Avoid/Transfer/Mitigate/Accept",
        "action_plan": "Detailed action plan",
        "estimated_effectiveness": 80,
        "implementation_complexity": "Medium",
        "resources_required": "Description of resources needed"
      }},
      ...
    ]
    """
    
    try:
        # Generate the response
        response = model.generate_content(prompt)
        
        # Parse the JSON response
        result = json.loads(response.text)
        return result
    
    except Exception as e:
        # Fallback if API call fails
        print(f"Error generating risk response suggestions: {e}")
        return [{
            "strategy": "Generic Risk Response",
            "type": "Mitigate",
            "action_plan": "Implement standard controls based on organization policy",
            "estimated_effectiveness": 50,
            "implementation_complexity": "Medium",
            "resources_required": "Standard resources"
        }]

def smart_risk_search(query: str, project_context: str = None) -> Dict[str, Any]:
    """
    Semantic search for risks using natural language understanding.
    
    Args:
        query: User's search query in natural language
        project_context: Optional context about the project
        
    Returns:
        Dictionary with search interpretation and search parameters
    """
    setup_gemini_api()
    
    # Initialize the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Create the prompt
    context = f"Project context: {project_context}" if project_context else "No specific project context provided"
    
    prompt = f"""
    As a risk management system assistant, interpret this natural language search query into structured search parameters.
    
    CONTEXT:
    {context}
    
    SEARCH QUERY:
    "{query}"
    
    INSTRUCTIONS:
    1. Identify key search parameters (categories, status, keywords, etc.)
    2. Extract any implicit filters (high risks, recent risks, etc.)
    3. Return a structured representation of the search intent
    4. Include both extracted parameters and a rewritten search query
    
    FORMAT YOUR RESPONSE AS JSON:
    {{
      "interpreted_intent": "A clear description of what the user is looking for",
      "search_parameters": {{
        "keywords": ["keyword1", "keyword2"],
        "categories": ["category1", "category2"],
        "status": ["status1", "status2"],
        "minimum_risk_score": 0-9 or null,
        "date_range": {{"from": "YYYY-MM-DD", "to": "YYYY-MM-DD"}} or null
      }},
      "rewritten_query": "The search query rewritten for better results"
    }}
    """
    
    try:
        # Generate the response
        response = model.generate_content(prompt)
        
        # Parse the JSON response
        result = json.loads(response.text)
        return result
    
    except Exception as e:
        # Fallback if API call fails
        print(f"Error processing smart search: {e}")
        return {
            "interpreted_intent": query,
            "search_parameters": {
                "keywords": [query],
                "categories": [],
                "status": [],
                "minimum_risk_score": None,
                "date_range": None
            },
            "rewritten_query": query
        }
