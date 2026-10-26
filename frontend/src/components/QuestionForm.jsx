import React, { useRef } from 'react';

/**
 * QuestionForm component supporting:
 * - Text prompt input area
 * - Real image upload with preview, file details, and removal
 * - Validation for file size (<5MB) and supported formats (JPG, PNG, WEBP)
 * - Dynamic action buttons with loading states
 */
export default function QuestionForm({
  question,
  onQuestionChange,
  imageFile,
  imagePreviewUrl,
  onImageSelect,
  loading,
  error,
  onSubmit,
  onClear,
}) {
  const fileInputRef = useRef(null);

  const handleBoxClick = () => {
    if (!loading && fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;

    // Validate size (< 5MB)
    const MAX_SIZE = 5 * 1024 * 1024;
    if (file.size > MAX_SIZE) {
      alert(`File size exceeds 5 MB (${(file.size / (1024 * 1024)).toFixed(2)} MB). Please select a smaller image.`);
      e.target.value = '';
      return;
    }

    // Validate type
    const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      alert('Unsupported image format. Please select a JPG, PNG, or WEBP image.');
      e.target.value = '';
      return;
    }

    onImageSelect(file);
  };

  const handleRemoveImage = (e) => {
    e.stopPropagation();
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    onImageSelect(null);
  };

  // Submission is allowed if either an image OR a non-empty question is provided
  const isSubmitDisabled = loading || (!question.trim() && !imageFile);

  return (
    <section className="panel-card">
      <div className="panel-header">
        <h2 className="panel-title">
          <span>2. Enter Question & Study Material</span>
        </h2>
        <span className="panel-title-badge">
          {imageFile ? 'Multimodal (Image + Text)' : 'Text Query'}
        </span>
      </div>

      <form onSubmit={onSubmit} className="form-group">
        <label htmlFor="question-input" className="form-label">
          {imageFile
            ? 'Question or focus area for this image (Optional)'
            : 'What would you like to study?'}
        </label>
        <textarea
          id="question-input"
          className="textarea-input"
          placeholder={
            imageFile
              ? 'E.g., What process does step B represent? Or leave empty for an overall explanation...'
              : 'E.g., Explain the Calvin cycle step-by-step, summarize Newton\'s laws for revision, or generate a quiz on photosynthesis...'
          }
          value={question}
          onChange={(e) => onQuestionChange(e.target.value)}
          disabled={loading}
          rows={3}
        />

        {error && (
          <div className="form-error-banner" role="alert">
            <span>⚠️</span>
            <span>{error}</span>
          </div>
        )}

        {/* Multimodal Image Upload Area */}
        <div className="form-group" style={{ marginTop: '0.5rem' }}>
          <div className="label-with-badge">
            <label className="form-label">Study Diagram / Photo</label>
            <span className="active-feature-pill">JPG, PNG, WEBP (Max 5 MB)</span>
          </div>

          {!imageFile ? (
            <div
              className="image-placeholder-box interactive"
              onClick={handleBoxClick}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') handleBoxClick();
              }}
            >
              <span className="image-placeholder-icon">📷</span>
              <div className="image-placeholder-title">
                Click or drag an image here to upload
              </div>
              <p className="image-placeholder-hint">
                Upload textbook diagrams, flowcharts, anatomical drawings, or handwritten notes.
              </p>
            </div>
          ) : (
            <div className="image-preview-container">
              <div className="preview-image-wrapper">
                <img
                  src={imagePreviewUrl}
                  alt="Study material preview"
                  className="preview-thumbnail"
                />
              </div>
              <div className="preview-info-wrapper">
                <div className="preview-filename">{imageFile.name}</div>
                <div className="preview-filesize">
                  {(imageFile.size / 1024).toFixed(1)} KB &bull; {imageFile.type}
                </div>
                <button
                  type="button"
                  className="btn-remove-image"
                  onClick={handleRemoveImage}
                  disabled={loading}
                >
                  ✕ Remove Image
                </button>
              </div>
            </div>
          )}

          <input
            ref={fileInputRef}
            type="file"
            accept="image/jpeg,image/png,image/webp,.jpg,.jpeg,.png,.webp"
            className="hidden-file-input"
            onChange={handleFileChange}
            disabled={loading}
          />
        </div>

        <div className="form-actions">
          <button
            type="button"
            className="btn-secondary"
            onClick={onClear}
            disabled={loading || (!question && !imageFile && !error)}
          >
            Clear
          </button>
          <button
            type="submit"
            className="btn-primary"
            disabled={isSubmitDisabled}
          >
            {loading ? (
              <span className="btn-loading-wrapper">
                <span className="btn-spinner"></span>
                <span>Gemma 4 is Analyzing...</span>
              </span>
            ) : imageFile ? (
              'Analyze Image with Gemma 4'
            ) : (
              'Ask Gemma 4'
            )}
          </button>
        </div>
      </form>
    </section>
  );
}
