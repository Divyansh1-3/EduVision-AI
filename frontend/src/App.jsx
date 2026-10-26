import React, { useState } from 'react';
import Header from './components/Header';
import ModeSelector from './components/ModeSelector';
import QuestionForm from './components/QuestionForm';
import ResponsePanel from './components/ResponsePanel';

/**
 * Root Application component for EduVision AI visual skeleton.
 */
export default function App() {
  const [selectedMode, setSelectedMode] = useState('explain');
  const [prompt, setPrompt] = useState('');
  const [selectedFileName, setSelectedFileName] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsSubmitted(true);
  };

  const handleClear = () => {
    setPrompt('');
    setSelectedFileName('');
    setIsSubmitted(false);
  };

  return (
    <div className="app-wrapper">
      <main className="main-container">
        <Header />

        <ModeSelector
          selectedMode={selectedMode}
          onSelectMode={(mode) => {
            setSelectedMode(mode);
            setIsSubmitted(false);
          }}
        />

        <QuestionForm
          prompt={prompt}
          onPromptChange={(val) => {
            setPrompt(val);
            if (isSubmitted) setIsSubmitted(false);
          }}
          selectedFileName={selectedFileName}
          onFileSelect={(name) => setSelectedFileName(name)}
          onSubmit={handleSubmit}
          onClear={handleClear}
        />

        <ResponsePanel
          selectedMode={selectedMode}
          isSubmitted={isSubmitted}
        />
      </main>

      <footer className="footer">
        <p>EduVision AI &bull; Incremental Prototype &bull; Hackathon Foundation</p>
      </footer>
    </div>
  );
}
