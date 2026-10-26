/**
 * Client service for calling the EduVision AI Study API.
 * Uses relative URLs (/api/study, /api/study/image) via Vite dev server proxy.
 */

/**
 * Submits a text-only study query (POST /api/study, application/json).
 */
export async function submitStudyQuery({ question, mode }) {
  if (!question || !question.trim()) {
    throw new Error('Please enter a question or topic before submitting.');
  }

  const response = await fetch('/api/study', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question: question.trim(),
      mode: mode,
    }),
  });

  if (!response.ok) {
    let errorMessage = 'Failed to generate study response. Please try again.';
    try {
      const errorJson = await response.json();
      if (errorJson && errorJson.detail) {
        if (typeof errorJson.detail === 'string') {
          errorMessage = errorJson.detail;
        } else if (Array.isArray(errorJson.detail)) {
          errorMessage = errorJson.detail
            .map((item) => item.msg || JSON.stringify(item))
            .join('; ');
        }
      }
    } catch {
      errorMessage = `Server request failed with status ${response.status} (${response.statusText}).`;
    }
    throw new Error(errorMessage);
  }

  return await response.json();
}

/**
 * Submits an image-based study query (POST /api/study/image, multipart/form-data).
 * Do NOT set Content-Type header manually; let the browser inject multipart/form-data with boundary.
 */
export async function submitStudyImageQuery({ imageFile, question, mode }) {
  if (!imageFile) {
    throw new Error('Please select an image file to upload.');
  }

  const formData = new FormData();
  formData.append('file', imageFile);
  formData.append('mode', mode || 'explain');
  if (question && question.trim()) {
    formData.append('question', question.trim());
  }

  const response = await fetch('/api/study/image', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    let errorMessage = 'Failed to process image study response. Please try again.';
    try {
      const errorJson = await response.json();
      if (errorJson && errorJson.detail) {
        if (typeof errorJson.detail === 'string') {
          errorMessage = errorJson.detail;
        } else if (Array.isArray(errorJson.detail)) {
          errorMessage = errorJson.detail
            .map((item) => item.msg || JSON.stringify(item))
            .join('; ');
        }
      }
    } catch {
      errorMessage = `Server request failed with status ${response.status} (${response.statusText}).`;
    }
    throw new Error(errorMessage);
  }

  return await response.json();
}
