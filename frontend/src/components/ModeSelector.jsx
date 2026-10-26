import React from 'react';

const STUDY_MODES = [
  {
    id: 'explain',
    title: 'Explain',
    icon: '💡',
    description: 'In-depth, structured conceptual explanations with real-world examples.',
  },
  {
    id: 'revision',
    title: 'Revision Notes',
    icon: '📝',
    description: 'Concise, high-yield bullet summaries, key terms, and memory anchors.',
  },
  {
    id: 'quiz',
    title: 'Quiz',
    icon: '🎯',
    description: 'Five practice questions with a separated answer key to test comprehension.',
  },
];

/**
 * ModeSelector component allowing the student to toggle between
 * Explain, Revision Notes, and Quiz study modes.
 */
export default function ModeSelector({ selectedMode, onSelectMode, disabled = false }) {
  return (
    <section className="panel-card">
      <div className="panel-header">
        <h2 className="panel-title">
          <span>1. Select Study Mode</span>
        </h2>
        <span className="panel-title-badge">3 modes available</span>
      </div>

      <div className="modes-grid" role="radiogroup" aria-label="Study Mode Selection">
        {STUDY_MODES.map((mode) => {
          const isActive = selectedMode === mode.id;
          return (
            <button
              key={mode.id}
              type="button"
              className={`mode-btn ${isActive ? 'active' : ''}`}
              onClick={() => !disabled && onSelectMode(mode.id)}
              disabled={disabled}
              role="radio"
              aria-checked={isActive}
            >
              <div className="mode-header">
                <span>{mode.icon}</span>
                <span>{mode.title}</span>
              </div>
              <p className="mode-desc">{mode.description}</p>
            </button>
          );
        })}
      </div>
    </section>
  );
}
