/**
 * Enhanced AI Analysis JavaScript Functions for Risk Management
 */

// Store project ID globally (will be set from template)
let PROJECT_ID = null;

function setProjectId(projectId) {
    PROJECT_ID = projectId;
}

function generateExecutiveSummaryWrapper() {
    const content = document.getElementById('executiveSummaryContent');
    content.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Generating executive summary...</p>
        </div>
    `;
    
    generateExecutiveSummary(PROJECT_ID, function(error, result) {
        if (error) {
            content.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
        } else {
            displayExecutiveSummary(result);
        }
    });
}

function analyzeRiskTrendsWrapper() {
    const content = document.getElementById('trendsContent');
    content.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Analyzing risk trends...</p>
        </div>
    `;
    
    analyzeRiskTrends(PROJECT_ID, function(error, result) {
        if (error) {
            content.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
        } else {
            displayTrendsAnalysis(result);
        }
    });
}

function analyzeRiskDependenciesWrapper() {
    const content = document.getElementById('dependenciesContent');
    content.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-info" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Analyzing risk dependencies...</p>
        </div>
    `;
    
    analyzeRiskDependencies(PROJECT_ID, function(error, result) {
        if (error) {
            content.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
        } else {
            displayDependenciesAnalysis(result);
        }
    });
}

function generateRiskResponseSuggestionsWrapper(riskId) {
    generateRiskResponseSuggestions(riskId, function(error, result) {
        if (error) {
            alert('Error: ' + error.message);
        } else {
            showResponseSuggestionsModal(result);
        }
    });
}

function showRiskScoringDemo() {
    const modal = new bootstrap.Modal(document.getElementById('demoModal'));
    document.getElementById('demoModalLabel').textContent = 'Risk Scoring Assistant Demo';
    document.getElementById('demoModalBody').innerHTML = `
        <div class="mb-3">
            <label class="form-label">Enter a risk description to get AI scoring suggestions:</label>
            <textarea class="form-control" id="scoringDemoText" rows="3" placeholder="e.g., Server hardware failure could cause system downtime..."></textarea>
        </div>
        <div class="mb-3">
            <label class="form-label">Category (Optional):</label>
            <select class="form-control" id="scoringDemoCategory">
                <option value="">Select category...</option>
                <option value="Technical">Technical</option>
                <option value="Financial">Financial</option>
                <option value="Operational">Operational</option>
                <option value="Legal">Legal</option>
            </select>
        </div>
    `;
    
    document.getElementById('demoActionBtn').onclick = function() {
        const description = document.getElementById('scoringDemoText').value;
        const category = document.getElementById('scoringDemoCategory').value;
        
        if (!description.trim()) {
            alert('Please enter a risk description');
            return;
        }
        
        aiRiskScoringAssistant(description, category, PROJECT_ID, function(error, result) {
            if (error) {
                alert('Error: ' + error.message);
            } else {
                modal.hide();
                showScoringModal(result);
            }
        });
    };
    
    modal.show();
}

function showCategorizationDemo() {
    const modal = new bootstrap.Modal(document.getElementById('demoModal'));
    document.getElementById('demoModalLabel').textContent = 'Auto Categorization Demo';
    document.getElementById('demoModalBody').innerHTML = `
        <div class="mb-3">
            <label class="form-label">Enter a risk description to get AI category suggestions:</label>
            <textarea class="form-control" id="categorizationDemoText" rows="3" placeholder="e.g., Potential data breach due to inadequate security measures..."></textarea>
        </div>
    `;
    
    document.getElementById('demoActionBtn').onclick = function() {
        const description = document.getElementById('categorizationDemoText').value;
        
        if (!description.trim()) {
            alert('Please enter a risk description');
            return;
        }
        
        autoCategorizeRisk(description, function(error, result) {
            if (error) {
                alert('Error: ' + error.message);
            } else {
                modal.hide();
                showCategorizationModal(result);
            }
        });
    };
    
    modal.show();
}

function showMonteCarloDemo() {
    const modal = new bootstrap.Modal(document.getElementById('demoModal'));
    document.getElementById('demoModalLabel').textContent = 'Monte Carlo Optimizer Demo';
    document.getElementById('demoModalBody').innerHTML = `
        <div class="mb-3">
            <label class="form-label">Enter a risk description for cost estimation:</label>
            <textarea class="form-control" id="montecarloDemoText" rows="3" placeholder="e.g., Equipment failure requiring replacement and repair..."></textarea>
        </div>
        <div class="mb-3">
            <label class="form-label">Category (Optional):</label>
            <select class="form-control" id="montecarloDemoCategory">
                <option value="">Select category...</option>
                <option value="Technical">Technical</option>
                <option value="Financial">Financial</option>
                <option value="Operational">Operational</option>
                <option value="Legal">Legal</option>
            </select>
        </div>
    `;
    
    document.getElementById('demoActionBtn').onclick = function() {
        const description = document.getElementById('montecarloDemoText').value;
        const category = document.getElementById('montecarloDemoCategory').value;
        
        if (!description.trim()) {
            alert('Please enter a risk description');
            return;
        }
        
        optimizeMonteCarloEstimates(description, category, PROJECT_ID, function(error, result) {
            if (error) {
                alert('Error: ' + error.message);
            } else {
                modal.hide();
                showMonteCarloModal(result);
            }
        });
    };
    
    modal.show();
}

function showTimelineForm() {
    const modal = new bootstrap.Modal(document.getElementById('timelineModal'));
    modal.show();
}

function generateTimeline() {
    const form = document.getElementById('timelineForm');
    const formData = new FormData(form);
    const constraints = {
        budget: formData.get('budget') ? parseInt(formData.get('budget')) : null,
        timeline: formData.get('timeline') || null,
        team_size: formData.get('team_size') ? parseInt(formData.get('team_size')) : null
    };
    
    const modal = bootstrap.Modal.getInstance(document.getElementById('timelineModal'));
    modal.hide();
    
    const content = document.getElementById('mitigationTimelineContent');
    content.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-success" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Generating mitigation timeline...</p>
        </div>
    `;
    
    generateMitigationTimeline(PROJECT_ID, constraints, function(error, result) {
        if (error) {
            content.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
        } else {
            displayMitigationTimeline(result);
        }
    });
}

function displayExecutiveSummary(summary) {
    const content = document.getElementById('executiveSummaryContent');
    
    let keyConcernsHtml = '';
    if (summary.key_concerns && summary.key_concerns.length > 0) {
        keyConcernsHtml = summary.key_concerns.map(concern => `
            <div class="col-md-4 mb-3">
                <div class="card border-${concern.urgency === 'High' ? 'danger' : concern.urgency === 'Medium' ? 'warning' : 'info'}">
                    <div class="card-body">
                        <h6 class="card-title">${concern.concern}</h6>
                        <p class="card-text small">${concern.business_impact}</p>
                        <span class="badge bg-${concern.urgency === 'High' ? 'danger' : concern.urgency === 'Medium' ? 'warning' : 'info'}">${concern.urgency} Urgency</span>
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    let recommendationsHtml = '';
    if (summary.strategic_recommendations && summary.strategic_recommendations.length > 0) {
        recommendationsHtml = summary.strategic_recommendations.map((rec, index) => `
            <div class="mb-3">
                <h6>${index + 1}. ${rec.recommendation}</h6>
                <p class="text-muted">${rec.rationale}</p>
                <small class="text-info"><strong>Timeline:</strong> ${rec.timeline}</small>
            </div>
        `).join('');
    }
    
    content.innerHTML = `
        <div class="mb-4">
            <h6>Executive Summary</h6>
            <p>${summary.executive_summary}</p>
        </div>
        
        ${summary.key_concerns && summary.key_concerns.length > 0 ? `
        <div class="mb-4">
            <h6>Key Concerns</h6>
            <div class="row">
                ${keyConcernsHtml}
            </div>
        </div>
        ` : ''}
        
        ${summary.financial_summary ? `
        <div class="mb-4">
            <h6>Financial Summary</h6>
            <div class="alert alert-light">
                <p><strong>Total Exposure:</strong> ${summary.financial_summary.total_exposure}</p>
                <p><strong>Budget Recommendations:</strong> ${summary.financial_summary.budget_recommendations}</p>
            </div>
        </div>
        ` : ''}
        
        ${summary.strategic_recommendations && summary.strategic_recommendations.length > 0 ? `
        <div class="mb-4">
            <h6>Strategic Recommendations</h6>
            ${recommendationsHtml}
        </div>
        ` : ''}
        
        ${summary.next_steps && summary.next_steps.length > 0 ? `
        <div>
            <h6>Next Steps</h6>
            <ul>
                ${summary.next_steps.map(step => `<li>${step}</li>`).join('')}
            </ul>
        </div>
        ` : ''}
    `;
}

function displayMitigationTimeline(timeline) {
    const content = document.getElementById('mitigationTimelineContent');
    
    let phasesHtml = '';
    if (timeline.timeline_phases && timeline.timeline_phases.length > 0) {
        phasesHtml = timeline.timeline_phases.map(phase => `
            <div class="col-md-6 mb-3">
                <div class="card">
                    <div class="card-header bg-success text-white">
                        <h6 class="mb-0">${phase.phase}</h6>
                        <small>Duration: ${phase.duration}</small>
                    </div>
                    <div class="card-body">
                        ${phase.responses.map(response => `
                            <div class="mb-2">
                                <strong>${response.strategy}</strong>
                                <br><small class="text-muted">Priority: ${response.priority} | Weeks ${response.start_week}-${response.start_week + response.duration_weeks - 1}</small>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    content.innerHTML = `
        <div class="mb-4">
            <h6>Timeline Summary</h6>
            <p>${timeline.risk_timeline_summary}</p>
        </div>
        
        ${phasesHtml ? `
        <div class="mb-4">
            <h6>Implementation Phases</h6>
            <div class="row">
                ${phasesHtml}
            </div>
        </div>
        ` : ''}
        
        ${timeline.quick_wins && timeline.quick_wins.length > 0 ? `
        <div class="mb-4">
            <h6>Quick Wins</h6>
            <div class="row">
                ${timeline.quick_wins.map(win => `
                    <div class="col-md-4 mb-2">
                        <div class="card border-success">
                            <div class="card-body">
                                <h6 class="card-title">${win.strategy}</h6>
                                <p class="card-text small">${win.benefit}</p>
                                <small class="text-muted">Effort: ${win.effort}</small>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
        ` : ''}
    `;
}

function displayTrendsAnalysis(analysis) {
    const content = document.getElementById('trendsContent');
    
    let patternsHtml = '';
    if (analysis.identified_patterns && analysis.identified_patterns.length > 0) {
        patternsHtml = analysis.identified_patterns.map(pattern => `
            <div class="card mb-3">
                <div class="card-body">
                    <h6 class="card-title">${pattern.pattern}</h6>
                    <p class="card-text">${pattern.description}</p>
                    <small class="text-muted">Affects risks: ${pattern.affected_risks.join(', ')}</small>
                </div>
            </div>
        `).join('');
    }
    
    let recommendationsHtml = '';
    if (analysis.mitigation_recommendations && analysis.mitigation_recommendations.length > 0) {
        recommendationsHtml = analysis.mitigation_recommendations.map(rec => `
            <li><strong>${rec.recommendation}</strong> - Addresses: ${rec.addresses_patterns.join(', ')}</li>
        `).join('');
    }
    
    content.innerHTML = `
        <div class="mb-4">
            <h6>Identified Patterns</h6>
            ${patternsHtml || '<p class="text-muted">No significant patterns identified.</p>'}
        </div>
        
        ${recommendationsHtml ? `
        <div class="mb-4">
            <h6>Mitigation Recommendations</h6>
            <ul>${recommendationsHtml}</ul>
        </div>
        ` : ''}
        
        ${analysis.potential_blind_spots && analysis.potential_blind_spots.length > 0 ? `
        <div class="alert alert-warning">
            <h6>Potential Blind Spots</h6>
            <ul class="mb-0">
                ${analysis.potential_blind_spots.map(spot => `<li>${spot}</li>`).join('')}
            </ul>
        </div>
        ` : ''}
    `;
}

function displayDependenciesAnalysis(analysis) {
    const content = document.getElementById('dependenciesContent');
    
    let dependenciesHtml = '';
    if (analysis.risk_dependencies && analysis.risk_dependencies.length > 0) {
        dependenciesHtml = analysis.risk_dependencies.map(dep => `
            <div class="card mb-3">
                <div class="card-body">
                    <h6 class="card-title">${dep.primary_risk}</h6>
                    <p class="card-text">${dep.impact_description}</p>
                    <div class="mt-2">
                        <span class="badge bg-primary">${dep.dependency_type}</span>
                        <small class="text-muted ms-2">Affects: ${dep.dependent_risks.join(', ')}</small>
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    let cascadesHtml = '';
    if (analysis.cascade_scenarios && analysis.cascade_scenarios.length > 0) {
        cascadesHtml = analysis.cascade_scenarios.map(cascade => `
            <div class="alert alert-warning">
                <h6>${cascade.trigger_risk}</h6>
                <p>${cascade.scenario_description}</p>
                <strong>Cascade Path:</strong> ${cascade.cascade_path.join(' → ')}
                <br><strong>Total Impact:</strong> <span class="badge bg-${cascade.total_impact === 'High' ? 'danger' : cascade.total_impact === 'Medium' ? 'warning' : 'info'}">${cascade.total_impact}</span>
            </div>
        `).join('');
    }
    
    content.innerHTML = `
        <div class="mb-4">
            <h6>Risk Dependencies</h6>
            ${dependenciesHtml || '<p class="text-muted">No significant dependencies identified.</p>'}
        </div>
        
        ${cascadesHtml ? `
        <div class="mb-4">
            <h6>Cascade Scenarios</h6>
            ${cascadesHtml}
        </div>
        ` : ''}
        
        ${analysis.critical_risks && analysis.critical_risks.length > 0 ? `
        <div class="alert alert-danger">
            <h6>Critical Risks</h6>
            <ul class="mb-0">
                ${analysis.critical_risks.map(risk => `<li><strong>${risk.risk}</strong> - ${risk.criticality_reason} (Affects ${risk.affected_risks_count} other risks)</li>`).join('')}
            </ul>
        </div>
        ` : ''}
    `;
}

function showCategorizationModal(categorization) {
    const modalBody = document.getElementById('aiResultsModalBody');
    const modalTitle = document.getElementById('aiResultsModalLabel');
    
    modalTitle.textContent = 'AI Risk Categorization';
    
    modalBody.innerHTML = `
        <div class="row">
            <div class="col-md-8">
                <div class="card border-success">
                    <div class="card-header bg-success text-white">
                        <h6 class="mb-0">Suggested Category: ${categorization.suggested_category}</h6>
                    </div>
                    <div class="card-body">
                        <p>${categorization.reasoning}</p>
                        <div class="mt-3">
                            <strong>Confidence:</strong> 
                            <div class="progress mt-1">
                                <div class="progress-bar" style="width: ${categorization.confidence * 100}%">${(categorization.confidence * 100).toFixed(0)}%</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        <h6 class="mb-0">Key Words Identified</h6>
                    </div>
                    <div class="card-body">
                        ${categorization.keywords_identified.map(keyword => `<span class="badge bg-secondary me-1">${keyword}</span>`).join('')}
                    </div>
                </div>
                
                ${categorization.alternative_categories.length > 0 ? `
                <div class="card mt-3">
                    <div class="card-header">
                        <h6 class="mb-0">Alternatives</h6>
                    </div>
                    <div class="card-body">
                        ${categorization.alternative_categories.map(alt => `<span class="badge bg-outline-secondary me-1">${alt}</span>`).join('')}
                    </div>
                </div>
                ` : ''}
            </div>
        </div>
    `;
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('aiResultsModal'));
    modal.show();
    
    // Handle apply button
    document.getElementById('aiResultsApplyBtn').onclick = function() {
        const categoryField = document.querySelector('select[name="category"]');
        if (categoryField) {
            // Find option by text content
            for (let option of categoryField.options) {
                if (option.text === categorization.suggested_category) {
                    option.selected = true;
                    break;
                }
            }
        }
        modal.hide();
    };
}

function showResponseSuggestionsModal(result) {
    const modalBody = document.getElementById('aiResultsModalBody');
    const modalTitle = document.getElementById('aiResultsModalLabel');
    
    modalTitle.textContent = `AI Response Suggestions - ${result.risk_title}`;
    
    let suggestionsHtml = '';
    if (result.suggestions && result.suggestions.length > 0) {
        suggestionsHtml = result.suggestions.map((suggestion, index) => `
            <div class="card mb-3">
                <div class="card-header bg-primary text-white">
                    <h6 class="mb-0">${index + 1}. ${suggestion.strategy} (${suggestion.type})</h6>
                </div>
                <div class="card-body">
                    <p>${suggestion.action_plan}</p>
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Effectiveness:</strong> ${suggestion.estimated_effectiveness}%
                        </div>
                        <div class="col-md-4">
                            <strong>Complexity:</strong> ${suggestion.implementation_complexity}
                        </div>
                        <div class="col-md-4">
                            <strong>Resources:</strong> ${suggestion.resources_required}
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    modalBody.innerHTML = suggestionsHtml || '<p class="text-muted">No suggestions available.</p>';
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('aiResultsModal'));
    modal.show();
    
    // Hide apply button for response suggestions
    document.getElementById('aiResultsApplyBtn').style.display = 'none';
}
