# AI Risk Scoring Assistant Guide

## Overview

The AI Risk Scoring Assistant is an advanced feature of the Risk Management System that leverages Google's Gemini-1.5-Flash model to provide intelligent likelihood and impact score suggestions with detailed reasoning and analysis.

## Features

### 🤖 Intelligent Risk Assessment
- **Automated Scoring**: Suggests likelihood (1-3) and impact (1-3) scores based on risk description and context
- **Detailed Reasoning**: Provides comprehensive explanations for each suggested score
- **Multi-perspective Analysis**: Considers technical, financial, operational, and timeline perspectives

### 📊 Comprehensive Analysis
- **Overall Risk Assessment**: Calculates risk score, level, and priority ranking
- **Key Factors Identification**: Lists critical factors influencing likelihood and impact
- **Historical Context**: References similar risks and industry patterns
- **Confidence Levels**: Indicates the AI's confidence in its assessment

### 📈 Actionable Insights
- **Monitoring Indicators**: Suggests specific metrics to track
- **Immediate Actions**: Recommends urgent steps to take
- **Affected Areas**: Identifies project areas that could be impacted
- **Escalation Thresholds**: Defines when to escalate concerns

## How to Use

### 1. Access the AI Risk Scoring Assistant

The AI Risk Scoring Assistant is available in two locations:

#### During Risk Creation
1. Navigate to a project
2. Click "Add New Risk"
3. Fill in the risk title and description
4. Click the **"AI Suggest"** button next to the Likelihood field

#### During Risk Editing
1. Open an existing risk for editing
2. Ensure title and description are filled
3. Click the **"AI Suggest"** button next to the Likelihood field

### 2. Using the AI Analysis

When you click "AI Suggest", the system will:

1. **Analyze** your risk description using advanced AI
2. **Generate** comprehensive scoring suggestions
3. **Display** results in an interactive modal window

### 3. Understanding the Results

The AI analysis provides:

#### Suggested Scores Section
- **Likelihood Score** (1-3) with percentage range
- **Impact Score** (1-3) with severity level
- **Overall Risk Assessment** with score, level, and priority

#### Analysis & Reasoning Section
- **Likelihood Reasoning**: Why this likelihood score was suggested
- **Impact Reasoning**: Detailed impact analysis
- **Assessment Summary**: Overall risk evaluation

#### Detailed Tabs
- **Key Factors**: Critical elements affecting the risk
- **Monitoring**: What to watch for and how often
- **Immediate Actions**: Steps to take right away

### 4. Applying Suggestions

After reviewing the AI analysis:

1. **Review** the suggested scores and reasoning
2. **Consider** the key factors and monitoring indicators
3. **Click "Apply AI Suggestions"** to use the recommended scores
4. **Modify** if needed based on your specific context
5. **Save** the risk with the updated scores

## AI Scoring Methodology

### Likelihood Assessment (1-3 Scale)

The AI evaluates likelihood based on:

- **Low (1)**: 0-33% probability within project timeframe
  - Rare occurrence in similar contexts
  - Strong preventive measures in place
  - Historical data shows infrequent occurrence

- **Medium (2)**: 34-66% probability within project timeframe
  - Moderate chance based on industry patterns
  - Some risk factors present
  - Mixed historical precedents

- **High (3)**: 67-100% probability within project timeframe
  - Strong indicators suggest likely occurrence
  - Multiple risk factors present
  - Historical data shows frequent occurrence

### Impact Assessment (1-3 Scale)

The AI evaluates impact considering:

- **Low (1)**: Minor impact (<10% effect on objectives)
  - Minimal disruption to timeline or budget
  - Easy to recover from
  - Limited scope of effect

- **Medium (2)**: Moderate impact (10-25% effect on objectives)
  - Noticeable but manageable disruption
  - Requires significant effort to address
  - Multiple areas affected

- **High (3)**: Major impact (>25% effect on objectives)
  - Severe disruption to project success
  - Difficult and costly to recover from
  - Wide-ranging consequences

### Overall Risk Calculation

- **Risk Score**: Likelihood × Impact (1-9 scale)
- **Risk Level**: Low (1-2), Medium (3-4), High (6-9)
- **Priority Ranking**: Critical, High, Medium, Low

## Best Practices

### 1. Provide Quality Input
- **Detailed Descriptions**: More context leads to better suggestions
- **Specific Information**: Include relevant technical, financial, or operational details
- **Clear Titles**: Use descriptive risk titles that capture the essence

### 2. Review AI Suggestions Critically
- **Consider Your Context**: AI suggestions are starting points, not absolute truth
- **Apply Domain Knowledge**: Your expertise matters in final decisions
- **Adjust as Needed**: Modify suggestions based on specific circumstances

### 3. Use Monitoring Indicators
- **Implement Tracking**: Set up monitoring for suggested indicators
- **Regular Reviews**: Check indicators at recommended frequencies
- **Early Warning**: Use thresholds for proactive risk management

### 4. Document Decisions
- **Reasoning**: Note why you accepted or modified AI suggestions
- **Context**: Record specific factors that influenced your decision
- **Updates**: Keep assessments current as project conditions change

## Integration with Existing Features

### Monte Carlo Simulation
- AI suggestions complement Monte Carlo analysis
- Use AI insights to refine cost impact estimates
- Consider AI-identified factors in simulation parameters

### Risk Response Planning
- AI monitoring indicators inform response strategies
- Immediate actions guide initial response planning
- Key factors help prioritize response efforts

### Reporting and Analytics
- AI confidence levels enhance report credibility
- Detailed reasoning supports audit requirements
- Comprehensive analysis improves risk communication

## Technical Requirements

### API Configuration
- Requires valid `GEMINI_API_KEY` in Django settings
- Internet connectivity for API calls
- Proper error handling for API failures

### Browser Compatibility
- Modern browsers with JavaScript support
- Bootstrap 5 for modal functionality
- AJAX support for real-time updates

## Troubleshooting

### Common Issues

#### "AI enhancement unavailable" Error
- **Check**: API key configuration
- **Verify**: Internet connectivity
- **Solution**: Review `GEMINI_API_KEY` in settings

#### Empty or Generic Suggestions
- **Cause**: Insufficient risk description
- **Solution**: Provide more detailed risk information
- **Tip**: Include specific context about your project

#### Slow Response Times
- **Normal**: AI analysis can take 5-10 seconds
- **Improvement**: More specific descriptions can speed up processing
- **Fallback**: Manual scoring is always available

### Error Messages

- **"Risk title and description are required"**: Fill in both fields before requesting AI analysis
- **"Error getting AI suggestions"**: Check network connection and API configuration
- **"AI analysis failed"**: Temporary API issue, try again or use manual scoring

## Security and Privacy

### Data Handling
- Risk descriptions are sent to Google's Gemini API
- No sensitive data is stored permanently by the AI service
- Standard data protection practices apply

### Best Practices
- Avoid including personally identifiable information in risk descriptions
- Use generic terms for sensitive business information
- Review your organization's AI usage policies

## Future Enhancements

### Planned Features
- **Learning from History**: AI will learn from your past risk assessments
- **Industry-Specific Models**: Tailored scoring for different sectors
- **Batch Analysis**: Process multiple risks simultaneously
- **Integration APIs**: Connect with external risk management tools

### Feedback and Improvement
- User feedback helps improve AI accuracy
- Regular model updates enhance performance
- Community insights inform feature development

## Support

### Getting Help
- Review this guide for common questions
- Check the main user manual for general system help
- Contact your system administrator for technical issues

### Feedback
- Report AI accuracy issues through the feedback system
- Suggest improvements for future versions
- Share use cases and success stories

---

**Note**: The AI Risk Scoring Assistant is designed to enhance, not replace, professional risk management judgment. Always apply critical thinking and domain expertise when making final risk assessment decisions.
