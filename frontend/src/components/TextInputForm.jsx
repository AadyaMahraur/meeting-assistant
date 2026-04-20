import React, { useState } from 'react';

const TextInputForm = ({ onSubmit, isLoading }) => {
  const [title, setTitle] = useState('');
  const [meetingDate, setMeetingDate] = useState('');
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ type: 'text', title, meetingDate, text });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-1">Title (Optional)</label>
        <input type="text" className="w-full border p-2 rounded" value={title} onChange={(e) => setTitle(e.target.value)} disabled={isLoading} />
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Date (Optional)</label>
        <input type="date" className="w-full border p-2 rounded" value={meetingDate} onChange={(e) => setMeetingDate(e.target.value)} disabled={isLoading} />
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">Meeting Transcript</label>
        <textarea required rows="5" className="w-full border p-2 rounded" placeholder="Paste notes here..." value={text} onChange={(e) => setText(e.target.value)} disabled={isLoading} />
      </div>
      <button type="submit" disabled={isLoading} className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:bg-gray-400">
        Submit Transcript
      </button>
    </form>
  );
};

export default TextInputForm;