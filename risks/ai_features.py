"""
AI-powered features for the Risk Management System using Google's Gemini 1.5 Flash
"""
import os
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import google.generativeai as genai
from django.conf import settings
from datetime import datetime

# Configure the Gemini API
def setup_gemini_api():
    """Initialize the Gemini API with the API key from settings"""
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in settings")
    genai.configure(api_key=api_key)

def extract_json_from_response(response_text: str) -> str:
    """
    Extract JSON content from Gemini response that may be wrapped in markdown code blocks.
    
    Args:
        response_text: Raw response text from Gemini
        
    Returns:
        Clean JSON string
    """
    # Remove markdown code block markers if present
    if '```json' in response_text:
        # Extract content between ```json and ```
        start_marker = '```json'
        end_marker = '```'
        start_idx = response_text.find(start_marker)
        if start_idx != -1:
            start_idx += len(start_marker)
            end_idx = response_text.find(end_marker, start_idx)
            if end_idx != -1:
                return response_text[start_idx:end_idx].strip()
    
    # If no markdown markers, return as is
    return response_text.strip()

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
    }}    """
    
    try:
        # Generate the response
        response = model.generate_content(prompt)
        
        # Extract clean JSON from response (handles markdown code blocks)
        clean_json = extract_json_from_response(response.text)
        
        # Parse the JSON response
        result = json.loads(clean_json)
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
        
        # Extract clean JSON from response (handles markdown code blocks)
        clean_json = extract_json_from_response(response.text)
        
        # Parse the JSON response
        result = json.loads(clean_json)
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
        
        # Extract clean JSON from response (handles markdown code blocks)
        clean_json = extract_json_from_response(response.text)
        
        # Parse the JSON response
        result = json.loads(clean_json)
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
        
        # Extract clean JSON from response (handles markdown code blocks)
        clean_json = extract_json_from_response(response.text)
        
        # Parse the JSON response
        result = json.loads(clean_json)
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
            },            "rewritten_query": query
        }

def ai_risk_scoring_assistant(risk_title: str, risk_description: str, 
                            risk_category: str = None, project_context: str = None) -> Dict[str, Any]:
    """
    AI Risk Scoring Assistant that suggests likelihood and impact scores with detailed reasoning.
    
    Args:
        risk_title: The title/name of the risk
        risk_description: Detailed description of the risk
        risk_category: Optional risk category (Technical, Financial, Operational, Legal)
        project_context: Optional context about the project
        
    Returns:
        Dictionary with suggested scores and detailed reasoning
    """
    setup_gemini_api()
    
    # Prepare context information
    context_info = []
    if risk_category:
        context_info.append(f"Risk Category: {risk_category}")
    if project_context:
        context_info.append(f"Project Context: {project_context}")
    
    context_text = "\n".join(context_info) if context_info else "No additional context provided"
    
    # Initialize the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Create the comprehensive prompt for risk scoring
    prompt = f"""
    As an expert risk management consultant with deep knowledge of risk assessment methodologies, 
    analyze this risk and provide likelihood and impact scores with detailed reasoning.
    
    RISK INFORMATION:
    Title: {risk_title}
    Description: {risk_description}
    {context_text}
    
    SCORING CRITERIA:
    
    LIKELIHOOD SCALE (1-3):
    - 1 (Low): 0-33% chance of occurring within project timeframe
    - 2 (Medium): 34-66% chance of occurring within project timeframe  
    - 3 (High): 67-100% chance of occurring within project timeframe
    
    IMPACT SCALE (1-3):
    - 1 (Low): Minor impact on project objectives, timeline, or budget (<10% impact)
    - 2 (Medium): Moderate impact on project objectives, timeline, or budget (10-25% impact)
    - 3 (High): Major impact on project objectives, timeline, or budget (>25% impact)
    
    ANALYSIS REQUIREMENTS:
    1. Analyze the risk from multiple perspectives (technical, financial, operational, timeline)
    2. Consider both direct and indirect consequences
    3. Factor in typical industry patterns and historical data
    4. Provide specific reasoning for each score
    5. Suggest key indicators to monitor
    6. Recommend immediate assessment actions
    
    FORMAT YOUR RESPONSE AS JSON:
    {{
      "suggested_likelihood": {{
        "score": 1-3,
        "percentage_range": "XX-XX%",
        "reasoning": "Detailed explanation for likelihood score",
        "key_factors": ["Factor 1", "Factor 2", "Factor 3"],
        "historical_precedents": "Similar risks and their frequency"
      }},
      "suggested_impact": {{
        "score": 1-3,
        "severity_level": "Low/Medium/High",
        "reasoning": "Detailed explanation for impact score",
        "affected_areas": ["Area 1", "Area 2", "Area 3"],
        "potential_consequences": [
          {{
            "consequence": "Specific consequence",
            "severity": "Low/Medium/High"
          }}
        ]
      }},
      "overall_risk_assessment": {{
        "risk_score": 1-9,
        "risk_level": "Low/Medium/High",
        "priority_ranking": "Critical/High/Medium/Low",
        "summary": "Overall risk assessment summary"
      }},
      "monitoring_indicators": [
        {{
          "indicator": "What to monitor",
          "frequency": "How often to check",
          "threshold": "When to escalate"
        }}
      ],
      "immediate_actions": [
        {{
          "action": "Specific action to take",
          "timeline": "When to complete",
          "responsible_party": "Who should do it"
        }}
      ],
      "confidence_level": "High/Medium/Low",
      "assessment_notes": "Additional insights or caveats"
    }}
    """
    
    try:
        # Generate the response
        response = model.generate_content(prompt)
        
        # Extract clean JSON from response (handles markdown code blocks)
        clean_json = extract_json_from_response(response.text)
        
        # Parse the JSON response
        result = json.loads(clean_json)
        
        # Add metadata
        result['ai_analysis_timestamp'] = str(datetime.now())
        result['model_used'] = 'gemini-1.5-flash'
        
        return result
    
    except Exception as e:
        # Fallback if API call fails
        print(f"Error in AI Risk Scoring Assistant: {e}")
        return {
            "suggested_likelihood": {
                "score": 2,
                "percentage_range": "30-60%",
                "reasoning": "AI scoring unavailable - default medium score assigned",
                "key_factors": ["AI analysis unavailable"],
                "historical_precedents": "Unable to analyze"
            },
            "suggested_impact": {
                "score": 2,
                "severity_level": "Medium",
                "reasoning": "AI scoring unavailable - default medium score assigned",
                "affected_areas": ["Unknown"],
                "potential_consequences": [{"consequence": "Unable to assess", "severity": "Medium"}]
            },
            "overall_risk_assessment": {
                "risk_score": 4,
                "risk_level": "Medium",
                "priority_ranking": "Medium",
                "summary": "AI assessment unavailable"
            },
            "monitoring_indicators": [{"indicator": "Manual assessment required", "frequency": "As needed", "threshold": "Human judgment"}],
            "immediate_actions": [{"action": "Conduct manual risk assessment", "timeline": "ASAP", "responsible_party": "Risk Manager"}],
            "confidence_level": "Low",
            "assessment_notes": f"AI analysis failed: {str(e)}"
        }

def auto_categorize_risk(risk_description: str, available_categories: List[str]) -> Dict[str, Any]:
    """
    Automatically suggest the most appropriate risk category based on description.
    
    Args:
        risk_description: The risk description to analyze
        available_categories: List of available category names
        
    Returns:
        Dictionary with suggested category and confidence
    """
    setup_gemini_api()
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    categories_text = ", ".join(available_categories)
    
    prompt = f"""
    As a risk management expert, categorize this risk based on its description.
    
    RISK DESCRIPTION: {risk_description}
    
    AVAILABLE CATEGORIES: {categories_text}
    
    INSTRUCTIONS:
    1. Analyze the risk description content
    2. Select the most appropriate category from the available options
    3. Provide reasoning for your choice
    4. Include confidence level and alternative suggestions if applicable
    
    FORMAT AS JSON:
    {{
      "suggested_category": "Category name from available list",
      "confidence": 0.0-1.0,
      "reasoning": "Clear explanation for category selection",
      "alternative_categories": ["alternative1", "alternative2"],
      "keywords_identified": ["keyword1", "keyword2"]
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # Extract clean JSON from response (handles markdown code blocks)

        clean_json = extract_json_from_response(response.text)

        result = json.loads(clean_json)
        
        # Ensure suggested category is in available categories
        if result["suggested_category"] not in available_categories:
            result["suggested_category"] = available_categories[0] if available_categories else "Technical"
            result["confidence"] = 0.3
            result["reasoning"] += " (Fallback to default category)"
            
        return result
    except Exception as e:
        print(f"Error in auto categorization: {e}")
        return {
            "suggested_category": available_categories[0] if available_categories else "Technical",
            "confidence": 0.2,
            "reasoning": "AI categorization unavailable - using default",
            "alternative_categories": [],
            "keywords_identified": []
        }

def optimize_monte_carlo_estimates(risk_description: str, category: str = None, 
                                  historical_data: List[Dict] = None) -> Dict[str, Any]:
    """
    AI suggests realistic cost estimates for Monte Carlo simulation based on risk analysis.
    
    Args:
        risk_description: The risk description to analyze
        category: Risk category for context
        historical_data: Optional historical cost data for similar risks
        
    Returns:
        Dictionary with suggested cost estimates and probability
    """
    setup_gemini_api()
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    context = f"Category: {category}" if category else "No category specified"
    historical_context = ""
    if historical_data:
        historical_context = "Historical cost data for similar risks:\n" + "\n".join([
            f"- {data.get('description', 'Unknown')}: ${data.get('cost', 0):,.2f}" 
            for data in historical_data[:3]
        ])
    
    prompt = f"""
    As a risk management and cost estimation expert, suggest realistic cost estimates for Monte Carlo simulation.
    
    RISK DESCRIPTION: {risk_description}
    CONTEXT: {context}
    {historical_context}
    
    INSTRUCTIONS:
    1. Analyze the risk to understand potential financial impact
    2. Suggest optimistic (best case), most likely, and pessimistic (worst case) cost estimates
    3. Suggest realistic probability percentage (1-100%)
    4. Provide reasoning for each estimate
    5. Consider both direct and indirect costs
    
    FORMAT AS JSON:
    {{
      "suggested_probability": 1-100,
      "optimistic_cost": 0.00,
      "most_likely_cost": 0.00,
      "pessimistic_cost": 0.00,
      "probability_reasoning": "Why this probability makes sense",
      "cost_reasoning": "Explanation of cost estimates",
      "cost_factors": ["factor1", "factor2", "factor3"],
      "confidence_level": "High/Medium/Low"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # Extract clean JSON from response (handles markdown code blocks)

        clean_json = extract_json_from_response(response.text)

        return json.loads(clean_json)
    except Exception as e:
        print(f"Error in Monte Carlo optimization: {e}")
        return {
            "suggested_probability": 25,
            "optimistic_cost": 1000.00,
            "most_likely_cost": 5000.00,
            "pessimistic_cost": 15000.00,
            "probability_reasoning": "Default moderate probability estimate",
            "cost_reasoning": "AI estimation unavailable - using conservative defaults",
            "cost_factors": ["Default estimation"],
            "confidence_level": "Low"
        }

def analyze_risk_dependencies(project_risks: List[Dict]) -> Dict[str, Any]:
    """
    Identify potential relationships and cascading effects between project risks.
    
    Args:
        project_risks: List of risk dictionaries with title, description, category, etc.
        
    Returns:
        Dictionary with identified dependencies and cascade effects
    """
    setup_gemini_api()
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    risks_text = ""
    for i, risk in enumerate(project_risks):
        risks_text += f"Risk {i+1}: {risk.get('title', 'Untitled')}\n"
        risks_text += f"  Category: {risk.get('category', 'N/A')}\n"
        risks_text += f"  Description: {risk.get('description', 'No description')}\n"
        risks_text += f"  Risk Score: {risk.get('risk_score', 'N/A')}\n\n"
    
    prompt = f"""
    As a risk management expert, analyze these project risks to identify dependencies and potential cascade effects.
    
    PROJECT RISKS:
    {risks_text}
    
    INSTRUCTIONS:
    1. Identify risks that could trigger or amplify other risks
    2. Find potential cascade effects (domino effects)
    3. Suggest risk clusters that should be managed together
    4. Identify critical risks that could impact multiple other risks
    5. Provide mitigation strategies for high-impact dependencies
    
    FORMAT AS JSON:
    {{
      "risk_dependencies": [
        {{
          "primary_risk": "Risk title",
          "dependent_risks": ["Risk title 1", "Risk title 2"],
          "dependency_type": "Triggers/Amplifies/Enables",
          "impact_description": "How the dependency works"
        }}
      ],
      "cascade_scenarios": [
        {{
          "trigger_risk": "Risk title",
          "cascade_path": ["Risk 1", "Risk 2", "Risk 3"],
          "total_impact": "High/Medium/Low",
          "scenario_description": "Description of cascade effect"
        }}
      ],
      "risk_clusters": [
        {{
          "cluster_name": "Cluster description",
          "risks": ["Risk 1", "Risk 2", "Risk 3"],
          "management_strategy": "How to manage this cluster together"
        }}
      ],
      "critical_risks": [
        {{
          "risk": "Risk title",
          "criticality_reason": "Why this risk is critical",
          "affected_risks_count": 3
        }}
      ]
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # Extract clean JSON from response (handles markdown code blocks)

        clean_json = extract_json_from_response(response.text)

        return json.loads(clean_json)
    except Exception as e:
        print(f"Error in risk dependency analysis: {e}")
        return {
            "risk_dependencies": [],
            "cascade_scenarios": [],
            "risk_clusters": [],
            "critical_risks": []
        }

def generate_executive_summary(project_risks: List[Dict], monte_carlo_results: Dict = None) -> Dict[str, Any]:
    """
    Create executive-friendly risk summaries with key insights and recommendations.
    
    Args:
        project_risks: List of project risks
        monte_carlo_results: Optional Monte Carlo simulation results
        
    Returns:
        Dictionary with executive summary components
    """
    setup_gemini_api()
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Prepare risk summary
    total_risks = len(project_risks)
    high_risks = len([r for r in project_risks if r.get('risk_score', 0) >= 6])
    medium_risks = len([r for r in project_risks if 3 <= r.get('risk_score', 0) < 6])
    low_risks = len([r for r in project_risks if r.get('risk_score', 0) < 3])
    
    risks_summary = f"Total risks: {total_risks} (High: {high_risks}, Medium: {medium_risks}, Low: {low_risks})"
    
    # Top risks for context
    top_risks = sorted(project_risks, key=lambda x: x.get('risk_score', 0), reverse=True)[:5]
    top_risks_text = "\n".join([
        f"- {risk.get('title', 'Untitled')} (Score: {risk.get('risk_score', 'N/A')}): {risk.get('description', 'No description')[:100]}..."
        for risk in top_risks
    ])
    
    monte_carlo_context = ""
    if monte_carlo_results:
        monte_carlo_context = f"Monte Carlo Results: Expected Value: ${monte_carlo_results.get('expected_value', 0):,.2f}, 95% Confidence: ${monte_carlo_results.get('percentile_95', 0):,.2f}"
    
    prompt = f"""
    As a senior risk management consultant, create an executive summary for project leadership.
    
    RISK OVERVIEW:
    {risks_summary}
    
    TOP RISKS:
    {top_risks_text}
    
    {monte_carlo_context}
    
    INSTRUCTIONS:
    Create a concise executive summary that includes:
    1. Overall risk posture assessment
    2. Key concerns that require leadership attention
    3. Financial impact summary (if Monte Carlo data available)
    4. Strategic recommendations
    5. Priority actions needed
    
    Write in business language, avoid technical jargon.
    
    FORMAT AS JSON:
    {{
      "executive_summary": "2-3 paragraph executive summary",
      "key_concerns": [
        {{
          "concern": "Brief concern description",
          "business_impact": "Impact in business terms",
          "urgency": "High/Medium/Low"
        }}
      ],
      "financial_summary": {{
        "total_exposure": "Financial exposure description",
        "key_cost_drivers": ["driver1", "driver2"],
        "budget_recommendations": "Budget-related recommendations"
      }},
      "strategic_recommendations": [
        {{
          "recommendation": "Strategic recommendation",
          "rationale": "Why this is important",
          "timeline": "When to implement"
        }}
      ],
      "next_steps": [
        "Immediate action 1",
        "Immediate action 2",
        "Immediate action 3"
      ]
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # Extract clean JSON from response (handles markdown code blocks)

        clean_json = extract_json_from_response(response.text)

        return json.loads(clean_json)
    except Exception as e:
        print(f"Error generating executive summary: {e}")
        return {
            "executive_summary": "Risk analysis unavailable. Manual review recommended.",
            "key_concerns": [],
            "financial_summary": {
                "total_exposure": "Analysis unavailable",
                "key_cost_drivers": [],
                "budget_recommendations": "Conduct manual assessment"
            },
            "strategic_recommendations": [],
            "next_steps": ["Conduct manual risk review"]
        }

def generate_mitigation_timeline(risk_responses: List[Dict], project_constraints: Dict = None) -> Dict[str, Any]:
    """
    AI suggests optimal sequencing and timing for risk response activities.
    
    Args:
        risk_responses: List of risk response strategies with details
        project_constraints: Optional project constraints (budget, timeline, resources)
        
    Returns:
        Dictionary with suggested timeline and prioritization
    """
    setup_gemini_api()
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    responses_text = ""
    for i, response in enumerate(risk_responses):
        responses_text += f"Response {i+1}: {response.get('strategy', 'Unknown Strategy')}\n"
        responses_text += f"  Risk: {response.get('risk_title', 'Unknown Risk')}\n"
        responses_text += f"  Type: {response.get('type', 'Unknown')}\n"
        responses_text += f"  Complexity: {response.get('implementation_complexity', 'Unknown')}\n"
        responses_text += f"  Effectiveness: {response.get('estimated_effectiveness', 'Unknown')}%\n"
        responses_text += f"  Resources: {response.get('resources_required', 'Unknown')}\n\n"
    
    constraints_text = ""
    if project_constraints:
        constraints_text = f"Project Constraints:\n"
        constraints_text += f"- Budget: {project_constraints.get('budget', 'Not specified')}\n"
        constraints_text += f"- Timeline: {project_constraints.get('timeline', 'Not specified')}\n"
        constraints_text += f"- Team Size: {project_constraints.get('team_size', 'Not specified')}\n"
    
    prompt = f"""
    As a project management and risk mitigation expert, create an optimal timeline for implementing these risk responses.
    
    RISK RESPONSES TO SCHEDULE:
    {responses_text}
    
    {constraints_text}
    
    INSTRUCTIONS:
    1. Prioritize responses based on risk severity, implementation complexity, and effectiveness
    2. Consider dependencies between responses
    3. Account for resource constraints and parallel execution opportunities
    4. Suggest realistic timeframes for each phase
    5. Identify quick wins vs. long-term initiatives
    
    FORMAT AS JSON:
    {{
      "timeline_phases": [
        {{
          "phase": "Phase 1: Immediate Actions",
          "duration": "1-2 weeks",
          "responses": [
            {{
              "strategy": "Response strategy",
              "priority": "High/Medium/Low",
              "start_week": 1,
              "duration_weeks": 2,
              "parallel_execution": true/false
            }}
          ]
        }}
      ],
      "quick_wins": [
        {{
          "strategy": "Quick win strategy",
          "benefit": "Expected benefit",
          "effort": "Implementation effort"
        }}
      ],
      "resource_allocation": {{
        "week_1_2": ["Activity 1", "Activity 2"],
        "week_3_4": ["Activity 3", "Activity 4"],
        "week_5_plus": ["Long-term activities"]
      }},
      "dependencies": [
        {{
          "dependent_response": "Response A",
          "prerequisite": "Response B must complete first",
          "reason": "Why this dependency exists"
        }}
      ],
      "risk_timeline_summary": "Overall timeline assessment and key milestones"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # Extract clean JSON from response (handles markdown code blocks)

        clean_json = extract_json_from_response(response.text)

        return json.loads(clean_json)
    except Exception as e:
        print(f"Error generating mitigation timeline: {e}")
        return {
            "timeline_phases": [{
                "phase": "Phase 1: Manual Planning Required",
                "duration": "TBD",
                "responses": []
            }],
            "quick_wins": [],
            "resource_allocation": {},
            "dependencies": [],
            "risk_timeline_summary": "AI timeline generation unavailable - manual planning required"
        }
