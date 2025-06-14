# 🤖 AI Configuration Guide

## Quick Setup

### 1. Get Your Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the generated API key

### 2. Configure Environment Variables
Open the `.env` file in your project root and replace `your-gemini-api-key-here` with your actual API key:

```bash
# Google Gemini API Key
GEMINI_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Install Dependencies (if needed)
```bash
pip install -r requirements.txt
```

### 4. Test the Setup
Run the setup script:
```bash
python setup_ai.py
```

## Detailed Configuration

### Environment Variables (.env file)

```bash
# Django Configuration
SECRET_KEY=your-django-secret-key
DEBUG=True

# Google Gemini API Configuration
GEMINI_API_KEY=your-gemini-api-key-here

# AI Features Settings
RISK_NOTIFY_HIGH_RISKS=True
RISK_NOTIFY_STATUS_CHANGE=True

# Database (currently using SQLite)
# DB_NAME=your_db_name
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
# DB_HOST=localhost
# DB_PORT=5432
```

### Django Settings (settings.py)

The following AI-related settings are automatically configured:

```python
# AI Features Configuration
AI_FEATURES_ENABLED = bool(GEMINI_API_KEY)  # Auto-enabled if API key exists
AI_REQUEST_TIMEOUT = 30  # Timeout for AI requests (seconds)
AI_MAX_RETRIES = 3  # Maximum retries for failed requests
AI_MODEL_NAME = 'gemini-1.5-flash'  # Gemini model to use
AI_TEMPERATURE = 0.1  # Lower temperature for consistent results
AI_MAX_OUTPUT_TOKENS = 2048  # Maximum response length
```

## API Key Security

### Development
- Store your API key in the `.env` file
- Never commit the `.env` file to version control
- The `.env` file is already in `.gitignore`

### Production
- Use environment variables or secure secret management
- Set `DEBUG=False` in production
- Use a strong `SECRET_KEY`

```bash
# Production environment variables
export GEMINI_API_KEY="your-actual-api-key"
export SECRET_KEY="your-production-secret-key" 
export DEBUG="False"
```

## Testing Your Configuration

### 1. Run the Setup Script
```bash
python setup_ai.py
```

### 2. Start the Development Server
```bash
python manage.py runserver
```

### 3. Test AI Features
1. Navigate to any project: `http://localhost:8000/`
2. Click **"Enhanced AI Analysis"**
3. Try the interactive demos for each AI feature

### 4. Verify API Connection
You can test the API connection directly:

```python
# In Django shell: python manage.py shell
from risks.ai_features import setup_gemini_api
setup_gemini_api()
print("✅ AI setup successful!")
```

## Available AI Features

### 🎯 Risk Scoring Assistant
- **URL**: `/ai/ai-risk-scoring/`
- **Function**: Suggests likelihood and impact scores with reasoning
- **Demo**: Available on Enhanced AI Analysis page

### 🏷️ Auto Risk Categorization
- **URL**: `/ai/auto-categorize-risk/`
- **Function**: Automatically suggests risk categories
- **Demo**: Available on Enhanced AI Analysis page

### 📊 Monte Carlo Optimizer
- **URL**: `/ai/optimize-monte-carlo/`
- **Function**: AI-optimized cost estimates for simulation
- **Demo**: Available on Enhanced AI Analysis page

### 🔗 Risk Dependency Analysis
- **URL**: `/ai/analyze-dependencies/{project_id}/`
- **Function**: Identifies risk relationships and cascade effects
- **Access**: Enhanced AI Analysis page

### 📋 Executive Summary Generator
- **URL**: `/ai/executive-summary/{project_id}/`
- **Function**: Creates business-friendly risk summaries
- **Access**: Enhanced AI Analysis page

### 📅 Mitigation Timeline Planner
- **URL**: `/ai/mitigation-timeline/`
- **Function**: Generates optimized timelines for risk responses
- **Access**: Enhanced AI Analysis page

## Troubleshooting

### Common Issues

#### 1. "GEMINI_API_KEY not set in settings"
**Solution**: Check your `.env` file and ensure the API key is correctly set:
```bash
GEMINI_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 2. "ModuleNotFoundError: No module named 'google.generativeai'"
**Solution**: Install the required package:
```bash
pip install google-generativeai>=0.3.0
```

#### 3. "403 Forbidden" API Error
**Possible causes**:
- Invalid API key
- API key doesn't have proper permissions
- Rate limit exceeded

**Solution**: 
- Verify your API key at [Google AI Studio](https://makersuite.google.com/app/apikey)
- Check API usage limits
- Ensure the API key has Generative AI permissions

#### 4. AI Features Not Working
**Debugging steps**:
1. Check if `AI_FEATURES_ENABLED` is `True` in Django shell:
   ```python
   from django.conf import settings
   print(settings.AI_FEATURES_ENABLED)
   ```

2. Test the API connection:
   ```python
   from risks.ai_features import setup_gemini_api
   setup_gemini_api()
   ```

3. Check the browser console for JavaScript errors

### Performance Optimization

#### API Rate Limits
- Gemini API has rate limits
- Implement request debouncing in JavaScript
- Consider caching responses for similar requests

#### Response Time
- Default timeout is 30 seconds
- Adjust `AI_REQUEST_TIMEOUT` if needed
- Show loading indicators for better UX

## Cost Management

### Gemini API Pricing
- Gemini 1.5 Flash is free for limited usage
- Monitor usage at [Google AI Studio](https://makersuite.google.com/app/apikey)
- Consider implementing usage tracking for production

### Cost Optimization Tips
1. **Cache Results**: Store AI responses for similar inputs
2. **Batch Requests**: Group multiple analyses when possible
3. **Optimize Prompts**: Shorter, more focused prompts cost less
4. **Set Limits**: Implement daily/monthly usage limits

## Security Best Practices

### API Key Protection
- Never expose API keys in client-side code
- Use environment variables for all deployments
- Rotate API keys regularly
- Monitor API key usage for anomalies

### Input Validation
- Sanitize user inputs before sending to AI
- Validate AI responses before displaying
- Implement rate limiting on endpoints
- Log AI interactions for audit trails

### Data Privacy
- Risk descriptions may contain sensitive information
- Consider data residency requirements
- Implement appropriate access controls
- Review data handling policies

## Deployment Checklist

### Pre-deployment
- [ ] Set `DEBUG=False`
- [ ] Configure production SECRET_KEY
- [ ] Set up production database
- [ ] Configure environment variables
- [ ] Test all AI features
- [ ] Set up monitoring and logging

### Production Environment
```bash
# Required environment variables
export SECRET_KEY="your-production-secret-key"
export DEBUG="False"
export GEMINI_API_KEY="your-gemini-api-key"
export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"

# Optional database configuration
export DB_NAME="risk_management_prod"
export DB_USER="risk_user"
export DB_PASSWORD="secure-password"
export DB_HOST="localhost"
export DB_PORT="5432"
```

## Support

### Documentation
- [Google AI Documentation](https://ai.google.dev/docs)
- [Django Documentation](https://docs.djangoproject.com/)
- [Project README](./README.md)

### Debugging
- Enable Django debug mode: `DEBUG=True`
- Check browser console for JavaScript errors
- Monitor Django logs for AI API errors
- Use Django shell for testing individual functions

### Getting Help
If you encounter issues:
1. Check this configuration guide
2. Review the troubleshooting section
3. Test with the provided setup script
4. Check the Django and browser logs

Your AI-powered risk management system should now be fully configured and ready to use! 🚀
