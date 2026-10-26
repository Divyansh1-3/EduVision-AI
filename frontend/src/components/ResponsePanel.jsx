import React from 'react';

/**
 * ResponsePanel component displaying the AI output.
 * Renders output safely as text without using raw HTML.
 */
export default function ResponsePanel({ selectedMode, hasImage = false, answer, loading, error }) {
  const modeDisplayNames = {
    explain: 'Explanation Mode',
    revision: 'Revision Notes Mode',
    quiz: 'Quiz Mode',
  };

  const currentModeTitle = modeDisplayNames[selectedMode] || 'Study Mode';

  return (
    <section className="panel-card">
      <div className="panel-header">
        <h2 className="panel-title">
          <span>3. AI Response</span>
        </h2>
        <span className="mode-active-badge">
          {hasImage ? `📷 Image ${currentModeTitle}` : currentModeTitle}
        </span>
      </div>

      {loading && (
        <div className="response-container loading-state" role="status">
          <div className="pulse-loader">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <h3 className="response-empty-heading">
            {hasImage
              ? `Gemma 4 is analyzing your diagram for ${currentModeTitle}...`
              : `Gemma 4 is synthesizing your ${currentModeTitle}...`}
          </h3>
          <p className="response-empty-text">
            Consulting the multimodal vision model and generating structured educational content.
          </p>
        </div>
      )}

      {!loading && error && (
        <div className="response-container error-state" role="alert">
          <div className="response-error-icon">⚠️</div>
          <h3 className="response-error-heading">Unable to Generate Study Response</h3>
          <p className="response-error-text">{error}</p>
        </div>
      )}

      {!loading && !error && answer && (
        <div className="response-result-card">
          <div className="result-header">
            <div className="result-meta">
              <span className="ai-source-tag">
                {hasImage ? '📷 Gemma 4 Vision Analysis' : '🤖 Gemma 4 Model Response'}
              </span>
              <span className="result-timestamp">Generated just now</span>
            </div>
          </div>
          {/* Render answer strictly as clean React text (no dangerouslySetInnerHTML) */}
          <div className="ai-response-text">
            {answer}
          </div>
        </div>
      )}

      {!loading && !error && !answer && (
        <div className="response-container empty-state">
          <div className="response-empty-icon">📖</div>
          <h3 className="response-empty-heading">Ready to Study</h3>
          <p className="response-empty-text">
            Select a mode, enter a question or upload a study diagram/photo above, and click <strong>Ask Gemma 4</strong>. Your tailored educational response will appear here.
          </p>
        </div>
      )}
    </section>
  );
}
