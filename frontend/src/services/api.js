import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// const apiClient = axios.create({
//   baseURL: API_BASE_URL,
//   headers: {
//     'Content-Type': 'application/json',
//   },
// });

// export default apiClient;

export const submitTextMeeting = async (title, meetingDate, text) => {
  const response = await fetch(`${API_BASE_URL}/meetings/text`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, meeting_date: meetingDate, text }),
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to submit text');
  }
  return response.json();
};

export const submitFileMeeting = async (title, meetingDate, file) => {
  const formData = new FormData();
  formData.append('file', file);
  if (title) formData.append('title', title);
  if (meetingDate) formData.append('meeting_date', meetingDate);

  const response = await fetch(`${API_BASE_URL}/meetings/upload`, {
    method: 'POST',
    body: formData, // No headers needed for FormData!
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to upload file');
  }
  return response.json();
};