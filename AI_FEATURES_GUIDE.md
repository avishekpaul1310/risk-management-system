# AI Features Guide for Risk Management System

This guide explains the AI capabilities added to your Risk Management System using Google's Gemini 1.5 Flash model. These features help streamline risk management workflows and provide intelligent insights without requiring any training data or complex machine learning setup.

## Getting Started

Before using these features, you need to:

1. Obtain a Google Gemini API key from the [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add your API key to the `.env` file:
   ```
   GEMINI_API_KEY=your-api-key-here
   ```
3. Install the required package:
   ```
   pip install google-generativeai
   ```

## Feature 1: Enhanced Risk Descriptions

**Where to access**: When creating or editing a risk, click the "Enhance" button next to the description field.

**What it does**: 
- Improves the clarity and specificity of your risk descriptions
- Ensures proper risk management terminology is used
- Provides a "clarity score" to measure the quality of your description
- Suggests specific improvements

**Best practices**:
- Start with at least a rough draft of your risk description
- The AI works best when you've already provided the basic information
- Review AI suggestions before accepting them

## Feature 2: Smart Risk Search

**Where to access**: On the project detail page, use the search bar at the top of the page.

**What it does**:
- Understands natural language queries like "show me high impact technical risks"
- Interprets your search intent and translates it to specific search parameters
- Returns matches from across your risks database

**Example queries**:
- "Critical financial risks with high impact"
- "Risks related to server downtime"
- "Risks with likelihood above 50% that are still open"
- "Regulatory compliance risks that are not mitigated"

## Feature 3: AI Risk Analysis

**Where to access**: On the project detail page, click the "AI Risk Analysis" button.

**What it does**:
- Analyzes patterns across all risks in your project
- Identifies common themes or potential blind spots
- Suggests mitigation strategies based on identified patterns
- Provides a comprehensive analysis of your project's risk landscape

**When to use**:
- After adding multiple risks to a project
- Before project reviews or stakeholder presentations
- When looking for insights across your risk register

## Feature 4: AI-Suggested Risk Responses

**Where to access**: On the risk detail page, click the "AI Suggestions" button in the Risk Responses section.

**What it does**:
- Generates tailored risk response strategies based on your risk details
- Creates multiple options across different response types (Avoid, Transfer, Mitigate, Accept)
- Estimates effectiveness and implementation complexity
- Describes required resources for each suggestion

**Best practices**:
- Consider multiple response strategies before selecting one
- The suggestions are starting points that you should adapt to your specific situation
- Always review and modify suggestions based on your organization's capabilities

## Limitations

- The AI is not familiar with your organization's specific context or risk appetite
- Suggestions should be reviewed and refined by human experts
- Complex or highly specialized risks may need additional expertise
- The model reflects general risk management practices, not industry-specific regulations

## Privacy & Data Usage

- The system sends only the minimal data needed for each feature (risk descriptions, titles, etc.)
- No risk data is stored by the AI service beyond the processing of each request
- Your API key usage is governed by Google's terms and conditions

## Troubleshooting

If you encounter any issues:

1. Check that your API key is correctly set in the `.env` file
2. Verify your internet connection, as these features require online access
3. If a feature returns an error, try again with more specific information
4. For persistent problems, check the Django error logs for more details
