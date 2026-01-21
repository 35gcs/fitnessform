import React from 'react'
import './AnalysisResults.css'

function AnalysisResults({ result, onReset }) {
  if (!result) return null

  const getScoreColor = (score) => {
    if (score >= 90) return '#10b981'
    if (score >= 75) return '#3b82f6'
    if (score >= 60) return '#f59e0b'
    return '#ef4444'
  }

  const getSeverityBadge = (severity) => {
    const colors = {
      critical: '#ef4444',
      warning: '#f59e0b',
      info: '#3b82f6'
    }
    return colors[severity] || '#6b7280'
  }

  return (
    <div className="analysis-results">
      <div className="results-card">
        <div className="results-header">
          <h2>{result.exercise} Form Analysis</h2>
          <button className="reset-button" onClick={onReset}>
            Analyze Another Video
          </button>
        </div>

        <div className="score-section">
          <div className="score-circle" style={{ borderColor: getScoreColor(result.overall_score) }}>
            <div className="score-value" style={{ color: getScoreColor(result.overall_score) }}>
              {result.overall_score}
            </div>
            <div className="score-label">Overall Score</div>
          </div>
          <div className="summary">
            <p>{result.summary}</p>
          </div>
        </div>

        {result.issues && result.issues.length > 0 && (
          <div className="section">
            <h3>Form Issues Detected</h3>
            <div className="issues-list">
              {result.issues.map((issue, index) => (
                <div key={index} className="issue-item">
                  <div className="issue-header">
                    <span
                      className="severity-badge"
                      style={{ backgroundColor: getSeverityBadge(issue.severity) }}
                    >
                      {issue.severity}
                    </span>
                    <h4>{issue.issue}</h4>
                  </div>
                  <p className="issue-description">{issue.description}</p>
                  {issue.timestamp && (
                    <p className="issue-timestamp">
                      Detected at: {issue.timestamp.toFixed(2)}s
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {result.recommendations && result.recommendations.length > 0 && (
          <div className="section">
            <h3>Recommendations</h3>
            <div className="recommendations-list">
              {result.recommendations.map((rec, index) => (
                <div key={index} className="recommendation-item">
                  <span className="recommendation-icon">💡</span>
                  <p>{rec}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {result.corrective_exercises && result.corrective_exercises.length > 0 && (
          <div className="section">
            <h3>Corrective Exercises</h3>
            <p className="section-subtitle">
              Incorporate these exercises into your training to address form issues
            </p>
            <div className="exercises-grid">
              {result.corrective_exercises.map((exercise, index) => (
                <div key={index} className="exercise-card">
                  <h4>{exercise.name}</h4>
                  <p className="exercise-description">{exercise.description}</p>
                  <div className="exercise-details">
                    <div className="detail">
                      <span className="detail-label">Sets:</span>
                      <span className="detail-value">{exercise.sets}</span>
                    </div>
                    <div className="detail">
                      <span className="detail-label">Reps:</span>
                      <span className="detail-value">{exercise.reps}</span>
                    </div>
                  </div>
                  <div className="exercise-focus">
                    <strong>Focus:</strong> {exercise.focus}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="next-steps">
          <h3>Next Steps</h3>
          <div className="next-steps-content">
            <p>1. Review the form issues and recommendations carefully</p>
            <p>2. Practice the corrective exercises 2-3 times per week</p>
            <p>3. Record another video in 2-4 weeks to track your progress</p>
            <p>4. Consider working with a qualified coach for hands-on guidance</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AnalysisResults
