# AI Integration Examples

This file demonstrates how to integrate with the AI features in your own custom views or components.

## Setting up the necessary imports

```python
from risks.ai_features import (
    enhance_risk_description,
    analyze_risk_trend,
    generate_risk_response_suggestions,
    smart_risk_search
)
```

## Example 1: Enhancing a Risk Description

```python
def enhance_my_risk_description(raw_description, category=None):
    """
    Enhance a risk description using AI
    
    Args:
        raw_description: The original description
        category: Optional category name
        
    Returns:
        Enhanced description and improvement suggestions
    """
    # Call the AI enhancement function
    result = enhance_risk_description(raw_description, category)
    
    # Extract the enhanced description
    enhanced_text = result.get('enhanced_description', raw_description)
    
    # Get improvement suggestions
    improvements = result.get('improvements', [])
    
    # Get sentiment and clarity score
    sentiment = result.get('sentiment', 'neutral')
    clarity_score = result.get('clarity_score', 5)
    
    return {
        'enhanced_text': enhanced_text,
        'improvements': improvements,
        'sentiment': sentiment,
        'clarity_score': clarity_score
    }
```

## Example 2: Analyzing Patterns in Risk Data

```python
def analyze_project_risks(project):
    """
    Analyze risks in a project to identify patterns
    
    Args:
        project: A Django Project model instance
        
    Returns:
        Analysis of risk patterns and recommendations
    """
    # Get all active risks for the project
    active_risks = project.risks.filter(status='Open')
    
    # Prepare data for analysis
    risk_titles = [risk.title for risk in active_risks]
    risk_descriptions = [risk.description for risk in active_risks]
    
    # Skip empty projects
    if not risk_titles:
        return {
            'error': 'No active risks found in project'
        }
    
    # Perform the analysis
    analysis_result = analyze_risk_trend(risk_titles, risk_descriptions)
    
    return analysis_result
```

## Example 3: Getting Risk Response Suggestions

```python
def get_response_suggestions_for_risk(risk):
    """
    Generate response suggestions for a specific risk
    
    Args:
        risk: A Django Risk model instance
        
    Returns:
        List of response strategies
    """
    # Get the category name
    category = risk.category.name if risk.category else "Uncategorized"
    
    # Call the AI function
    suggestions = generate_risk_response_suggestions(
        risk.description,
        category,
        risk.likelihood,
        risk.impact
    )
    
    return suggestions
```

## Example 4: Natural Language Risk Search

```python
def search_risks_with_natural_language(query, project=None):
    """
    Search for risks using natural language
    
    Args:
        query: Natural language search query
        project: Optional Project instance for context
        
    Returns:
        Interpreted search parameters and query
    """
    # Get project context if available
    project_context = None
    if project:
        project_context = f"Project: {project.name} - {project.description}"
    
    # Perform the search interpretation
    search_result = smart_risk_search(query, project_context)
    
    # Extract search parameters
    params = search_result.get('search_parameters', {})
    
    # Build a filter for the database query
    filter_kwargs = {}
    
    # Handle keywords (basic text search in title and description)
    keywords = params.get('keywords', [])
    
    # Base queryset - filter by project if provided
    if project:
        risks = project.risks.all()
    else:
        risks = Risk.objects.all()
    
    # Filter by keywords
    if keywords:
        from django.db.models import Q
        keyword_filter = Q()
        for keyword in keywords:
            if keyword:
                keyword_filter |= Q(title__icontains=keyword) | Q(description__icontains=keyword)
        risks = risks.filter(keyword_filter)
    
    # Apply other filters
    if params.get('categories'):
        risks = risks.filter(category__name__in=params.get('categories'))
    
    if params.get('status'):
        risks = risks.filter(status__in=params.get('status'))
    
    # Return both the search interpretation and the filtered risks
    return {
        'interpreted_intent': search_result.get('interpreted_intent'),
        'rewritten_query': search_result.get('rewritten_query'),
        'risks': risks
    }
```

## JavaScript Integration Example

Here's an example of how to use the AI features from JavaScript:

```javascript
// Example: Risk description enhancement
function enhanceDescription() {
    const descriptionField = document.getElementById('id_description');
    const categoryField = document.getElementById('id_category');
    const enhanceBtn = document.getElementById('enhanceBtn');
    
    const description = descriptionField.value;
    const categoryId = categoryField.value;
    
    // Show loading state
    enhanceBtn.disabled = true;
    enhanceBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Enhancing...';
    
    // Call the API
    fetch('/ai/enhance-risk-description/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({
            description: description,
            category_id: categoryId
        })
    })
    .then(response => response.json())
    .then(data => {
        // Reset button state
        enhanceBtn.disabled = false;
        enhanceBtn.innerHTML = 'Enhance';
        
        if (data.success) {
            // Show the enhanced description
            descriptionField.value = data.enhanced_description;
            
            // Show improvements
            showImprovements(data.improvements);
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        // Reset button state
        enhanceBtn.disabled = false;
        enhanceBtn.innerHTML = 'Enhance';
        
        alert('Error: ' + error);
    });
}

// Helper function to get CSRF token
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
```
