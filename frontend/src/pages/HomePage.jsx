import NavBar from '../components/Navigation.jsx';
import { submitTextMeeting, submitFileMeeting } from '../services/api';
import { useNavigate } from 'react-router-dom';
import React, { useState } from 'react';
import TextInputForm from '../components/TextInputForm';
import FileUploadForm from '../components/FileUploadForm';
import ProcessingIndicator from '../components/ProcessingIndicator';


const HomePage = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('text');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmission = async (formData) => {
    setIsLoading(true);
    setError(null);

    try {
      let data;
      if (formData.type === 'text') {
        data = await submitTextMeeting(formData.title, formData.meetingDate, formData.text);
      } else {
        data = await submitFileMeeting(formData.title, formData.meetingDate, formData.file);
      }
      
      navigate(`/results/${data.meeting_id}`);
      
    } catch (err) {
      setError(err.message);
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 mt-10 bg-white rounded-xl shadow-lg">
      <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">Meeting AI Assistant</h1>
      
      {isLoading ? (
        <ProcessingIndicator />
      ) : (
        <>
          {/* Tabs */}
          <div className="flex border-b mb-6">
            <button 
              className={`flex-1 py-3 font-medium transition-colors ${activeTab === 'text' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
              onClick={() => setActiveTab('text')}
            >
              Text Upload
            </button>
            <button 
              className={`flex-1 py-3 font-medium transition-colors ${activeTab === 'file' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500 hover:text-gray-700'}`}
              onClick={() => setActiveTab('file')}
            >
              File Upload
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}

          {/* Form Rendering */}
          {activeTab === 'text' ? (
            <TextInputForm onSubmit={handleSubmission} isLoading={isLoading} />
          ) : (
            <FileUploadForm onSubmit={handleSubmission} isLoading={isLoading} />
          )}
        </>
      )}
    </div>
  );
};

export default HomePage;