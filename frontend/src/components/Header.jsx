import React from 'react';

/**
 * Header component displaying EduVision AI branding and mission subtitle.
 */
export default function Header() {
  return (
    <header className="header-container">
      <div className="brand-badge">
        <span className="pulse-dot"></span>
        <span>Gemma 4 Powered &bull; Multimodal Study Assistant</span>
      </div>
      <h1 className="main-title">EduVision AI</h1>
      <p className="main-subtitle">
        Your multimodal study companion for visual explanations, rapid revision notes, and interactive self-quizzes.
      </p>
    </header>
  );
}
