/**
 * JavaScript functions for interacting with AI features
 */

/**
 * Enhances a risk description using Gemini AI
 * @param {string} description - The original risk description
 * @param {string} category - Optional risk category
 * @param {function} callback - Callback function to handle the enhanced description
 */
function enhanceRiskDescription(description, category, callback) {
    // Create request data
    const requestData = {
        description: description,
        category: category
    };
    
    // Send AJAX request
    fetch('/ai/enhance-risk-description/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            callback(null, data);
        } else {
            callback(new Error(data.error || 'Failed to enhance description'), null);
        }
    })
    .catch(error => {
        callback(error, null);
    });
}

/**
 * Analyzes trends in project risks
 * @param {number} projectId - ID of the project
 * @param {function} callback - Callback function to handle the analysis results
 */
function analyzeRiskTrends(projectId, callback) {
    // Send AJAX request
    fetch(`/ai/analyze-risk-trends/${projectId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            callback(null, data);
        } else {
            callback(new Error(data.message || 'Failed to analyze risk trends'), null);
        }
    })
    .catch(error => {
        callback(error, null);
    });
}

/**
 * Generates risk response suggestions
 * @param {number} riskId - ID of the risk
 * @param {function} callback - Callback function to handle the suggestions
 */
function generateRiskResponseSuggestions(riskId, callback) {
    // Send AJAX request
    fetch(`/ai/generate-response-suggestions/${riskId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            callback(null, data);
        } else {
            callback(new Error(data.error || 'Failed to generate suggestions'), null);
        }
    })
    .catch(error => {
        callback(error, null);
    });
}

/**
 * Performs a smart risk search using natural language
 * @param {string} query - The search query
 * @param {number} projectId - Optional project ID for context
 * @param {function} callback - Callback function to handle the search results
 */
function smartRiskSearch(query, projectId, callback) {
    // Create request data
    const requestData = {
        query: query,
        project_id: projectId || null
    };
    
    // Send AJAX request
    fetch('/ai/smart-risk-search/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            callback(null, data);
        } else {
            callback(new Error(data.error || 'Failed to process search'), null);
        }
    })
    .catch(error => {
        callback(error, null);
    });
}

/**
 * AI-powered risk scoring assistant
 * @param {string} description - Risk description to analyze
 * @param {string} category - Optional risk category
 * @param {number} projectId - Optional project ID for context
 * @param {function} callback - Callback function to handle the scoring suggestions
 */
function aiRiskScoringAssistant(description, category, projectId, callback) {
    const requestData = {
        description: description,
        category: category || null,
        project_id: projectId || null
    };
    
    fetch('/ai/ai-risk-scoring/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            callback(null, data.scoring_suggestion);
        } else {
            callback(new Error(data.error || 'Failed to get scoring suggestions'), null);
        }
    })
    .catch(error => {
        callback(error, null);
    });
}

/**
 * Auto-categorize risk using AI
 * @param {string} description - Risk description to categorize
 * @param {function} callback - Callback function to handle the categorization
 */
function autoCategorizeRisk(description, callback) {
    const requestData = {
        description: description
    };
    
    fetch('/ai/auto-categorize-risk/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            callback(null, data.categorization);
        } else {
            callback(new Error(data.error || 'Failed to categorize risk'), null);
        }
    })
    .catch(error => {
        callback(error, null);
    });
}

/**
 * Optimize Monte Carlo estimates using AI
 * @param {string} description - Risk description
 * @param {string} category - Risk category
 * @param {number} projectId - Optional project ID for historical context
 * @param {function} callback - Callback function to handle the estimates
 */
function optimizeMonteCarloEstimates(description, category, projectId, callback) {
    const requestData = {
        description: description,
        category: category || null,
        project_id: projectId || null
    };
    
    fetch('/ai/optimize-monte-carlo/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            callback(null, data.monte_carlo_suggestions);
        } else {
            callback(new Error(data.error || 'Failed to optimize Monte Carlo estimates'), null);
        }
    })
    .catch(error => {
        callback(error, null);
    });
}

/**
 * Analyze risk dependencies for a project
 * @param {number} projectId - Project ID
 * @param {function} callback - Callback function to handle the analysis
 */
function analyzeRiskDependencies(projectId, callback) {
    fetch(`/ai/analyze-dependencies/${projectId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            callback(null, data);
        } else {
            callback(new Error(data.error || 'Failed to analyze dependencies'), null);
        }
    })
    .catch(error => {
        callback(error, null);
    });
}

/**
 * Generate executive summary for a project
 * @param {number} projectId - Project ID
 * @param {function} callback - Callback function to handle the summary
 */
function generateExecutiveSummary(projectId, callback) {
    fetch(`/ai/executive-summary/${projectId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            callback(null, data);
        } else {
            callback(new Error(data.error || 'Failed to generate summary'), null);
        }
    })
    .catch(error => {
        callback(error, null);
    });
}

/**
 * Generate mitigation timeline for project risks
 * @param {number} projectId - Project ID
 * @param {object} constraints - Optional project constraints
 * @param {function} callback - Callback function to handle the timeline
 */
function generateMitigationTimeline(projectId, constraints, callback) {
    const requestData = {
        project_id: projectId,
        constraints: constraints || {}
    };

    fetch('/ai/mitigation-timeline/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            callback(null, data);
        } else {
            callback(new Error(data.error || 'Failed to generate timeline'), null);
        }
    })
    .catch(error => {
        callback(error, null);
    });
}

/**
 * Helper function to get CSRF token from cookies
 * @returns {string} CSRF token
 */
function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    
    return cookieValue || '';
}

// Create modal for showing AI results
function createAiModal() {
    // Check if modal already exists
    if (document.getElementById('aiResultsModal')) {
        return;
    }
    
    // Create modal HTML
    const modalHtml = `
    <div class="modal fade" id="aiResultsModal" tabindex="-1" aria-labelledby="aiResultsModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="aiResultsModalLabel">AI Results</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body" id="aiResultsModalBody">
                    <!-- Content will be dynamically inserted -->
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-primary" id="aiResultsApplyBtn">Apply</button>
                </div>
            </div>
        </div>
    </div>
    `;
    
    // Append modal to body
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    createAiModal();
});
