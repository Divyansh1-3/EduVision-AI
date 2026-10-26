import React, { useRef } from 'react';

/**
 * QuestionForm component containing:
 * - Text prompt input area
 * - Visual placeholder for image selection
 * - Action buttons
 */
export default function QuestionForm({
  prompt,
  onPromptChange,
  selectedFileName,
  onFileSelect,
  onSubmit,
  onClear,
}) {
  const fileInputRef = useRef(null);

  const handleBoxClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files && e.target.files[0];
    if (file) {
      onFileSelect(file.name);
    }
  };

  return (
    <section className="panel-card">
      <div className="panel-header">
        <h2 className="panel-title">
          <span>2. Enter Question & Diagram</span>
        </h2>
        <span className="panel-title-badge">Multimodal Input</span>
      </div>

      <form onSubmit={onSubmit} className="form-group">
        <label htmlFor="prompt-input" className="form-label">
          What would you like to study?
        </label>
        <textarea
          id="prompt-input"
          className="textarea-input"
          placeholder="E.g., Explain the Calvin cycle diagram, summarize key points of mitosis, or create a quiz on Ohm's Law..."
          value={prompt}
          onChange={(e) => onPromptChange(e.target.value)}
        />

        <div className="form-group" style={{ marginTop: '0.5rem' }}>
          <label className="form-label">Study Material / Diagram (Optional)</label>
          <div
            className="image-placeholder-box"
            onClick={handleBoxClick}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') handleBoxClick();
            }}
          >
            <span className="image-placeholder-icon">📷</span>
            <div className="image-placeholder-title">
              {selectedFileName ? (
                <span className="selected-file-pill">
                  📎 {selectedFileName}
                </span>
              ) : (
                'Image Selection Placeholder — Click to browse'
              )}
            </div>
            <p className="image-placeholder-hint">
              Upload textbook pages, diagrams, or handwritten notes. (Multimodal ingestion planned for Step 2)
            </p>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              className="hidden-file-input"
              onChange={handleFileChange}
            />
          </div>
        </div>

        <div className="form-actions">
          <button
            type="button"
            className="btn-secondary"
            onClick={onClear}
          >
            Clear
          </button>
          <button
            type="submit"
            className="btn-primary"
          >
            Send to AI (Skeleton)
          </button>
        </div>
      </form>
    </section>
  );
}
