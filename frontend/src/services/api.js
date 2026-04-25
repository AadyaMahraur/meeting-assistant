const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

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
    body: formData, 
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to upload file');
  }
  return response.json();
};

export const getMeetingDetail = async (id) => {
  const response = await fetch(`${API_BASE_URL}/meetings/${id}`);
  if (!response.ok) throw new Error('Meeting not found');
  return response.json();
};

export const getMeetingStatus = async (id) => {
  const response = await fetch(`${API_BASE_URL}/meetings/${id}/status`);
  if (!response.ok) throw new Error('Could not fetch status');
  return response.json();
};

export const getAllMeetings = async (page = 1, perPage = 9) => {
  const response = await fetch(`${API_BASE_URL}/meetings/?page=${page}&per_page=${perPage}`);
  if (!response.ok) throw new Error('Failed to fetch meeting history');
  return response.json();
};

export const searchMeetings = async (query, page = 1, perPage = 9) => {
  const response = await fetch(
    `${API_BASE_URL}/meetings/search?q=${encodeURIComponent(query)}&page=${page}&per_page=${perPage}`
  );
  if (!response.ok) throw new Error("Search Failed");
  return response.json();
};

export const deleteMeeting = async (meetingId) => {
    const response = await fetch(`${API_BASE_URL}/meetings/${meetingId}`, {
        method: 'DELETE',
    });
    
    if (!response.ok) {
        throw new Error("Failed to delete meeting");
    }
    
    return response.json();
};