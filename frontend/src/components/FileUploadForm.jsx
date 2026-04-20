import React, { useState } from 'react';

const FileUploadForm = ({ onSubmit, isLoading }) => {
  const [title, setTitle] = useState('');
  const [meetingDate, setMeetingDate] = useState('');
  const [file, setFile] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ type: 'file', title, meetingDate, file });
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
        <label className="block text-sm font-medium mb-1">Upload Document (.txt, .md, .docx)</label>
        <input type="file" required accept=".txt,.md,.docx" className="w-full border p-2 rounded" onChange={(e) => setFile(e.target.files[0])} disabled={isLoading} />
      </div>
      <button type="submit" disabled={isLoading || !file} className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:bg-gray-400">
        Upload File
      </button>
    </form>
  );
};

export default FileUploadForm;