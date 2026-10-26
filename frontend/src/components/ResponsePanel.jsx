import React from 'react';

/**
 * ResponsePanel component displaying the placeholder response area.
 * Visual skeleton only - does not mock AI answers.
 */
export default function ResponsePanel({ selectedMode, isSubmitted }) {
  const modeDisplayNames = {
    explain: 'Explanation Mode',
    revision: 'Revision Notes Mode',
    quiz: 'Quiz Mode',
  };

  return (
    <section className="panel-card">
      <div className="panel-header">
        <h2 className="panel-title">
          <span>3. AI Response Panel</span>
        </h2>
        <span className="skeleton-badge">
          {modeDisplayNames[selectedMode] || 'Explain Mode'}
        </span>
      </div>

      <div className="response-container">
        <div className="response-empty-icon">📖</div>
        <h3 className="response-empty-heading">
          {isSubmitted
            ? 'Skeleton UI Demonstration Active'
            : 'Response Output Placeholder'}
        </h3>
        <p className="response-empty-text">
          {isSubmitted
            ? 'Your input has been received by the interface. AI response generation via Gemma 4 and the official google-genai SDK will be connected in subsequent steps.'
            : 'Select a study mode, type a question, or choose an optional diagram above. AI-generated answers will be rendered here once the backend services are linked.'}
        </p>
      </div>
    </section>
  );
}
