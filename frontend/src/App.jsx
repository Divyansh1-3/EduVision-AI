import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import ModeSelector from './components/ModeSelector';
import QuestionForm from './components/QuestionForm';
import ResponsePanel from './components/ResponsePanel';
import { submitStudyQuery, submitStudyImageQuery } from './services/studyApi';

/**
 * Root Application component for EduVision AI.
 * Connects UI state to the FastAPI backend and Gemma 4 multimodal service.
 */
export default function App() {
  const [selectedMode, setSelectedMode] = useState('explain');
  const [question, setQuestion] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState(null);
  const [error, setError] = useState(null);

  // Clean up object URLs to prevent browser memory leaks
  useEffect(() => {
    return () => {
      if (imagePreviewUrl) {
        URL.revokeObjectURL(imagePreviewUrl);
      }
    };
  }, [imagePreviewUrl]);

  const handleImageSelect = (file) => {
    if (imagePreviewUrl) {
      URL.revokeObjectURL(imagePreviewUrl);
    }

    if (file) {
      setImageFile(file);
      setImagePreviewUrl(URL.createObjectURL(file));
    } else {
      setImageFile(null);
      setImagePreviewUrl(null);
    }
    if (error) setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const trimmedQuestion = question.trim();
    if (!trimmedQuestion && !imageFile) {
      setError('Please enter a question or select an image to study.');
      return;
    }

    setLoading(true);
    setError(null);
    setAnswer(null);

    try {
      let data;
      if (imageFile) {
        // Use multipart image endpoint
        data = await submitStudyImageQuery({
          imageFile,
          question: trimmedQuestion,
          mode: selectedMode,
        });
      } else {
        // Use standard JSON endpoint
        data = await submitStudyQuery({
          question: trimmedQuestion,
          mode: selectedMode,
        });
      }
      setAnswer(data.answer);
    } catch (err) {
      setError(err.message || 'An unexpected error occurred while communicating with the server.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setQuestion('');
    if (imagePreviewUrl) {
      URL.revokeObjectURL(imagePreviewUrl);
    }
    setImageFile(null);
    setImagePreviewUrl(null);
    setAnswer(null);
    setError(null);
  };

  const handleModeChange = (mode) => {
    setSelectedMode(mode);
    if (error) setError(null);
  };

  return (
    <div className="app-wrapper">
      <main className="main-container">
        <Header />

        <ModeSelector
          selectedMode={selectedMode}
          onSelectMode={handleModeChange}
          disabled={loading}
        />

        <QuestionForm
          question={question}
          onQuestionChange={(val) => {
            setQuestion(val);
            if (error) setError(null);
          }}
          imageFile={imageFile}
          imagePreviewUrl={imagePreviewUrl}
          onImageSelect={handleImageSelect}
          loading={loading}
          error={error}
          onSubmit={handleSubmit}
          onClear={handleClear}
        />

        <ResponsePanel
          selectedMode={selectedMode}
          hasImage={Boolean(imageFile)}
          answer={answer}
          loading={loading}
          error={error}
        />
      </main>

      <footer className="footer">
        <p>EduVision AI &bull; Powered by Gemma 4 Multimodal &bull; Hackathon Edition</p>
      </footer>
    </div>
  );
}
