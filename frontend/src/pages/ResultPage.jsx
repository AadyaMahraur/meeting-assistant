import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom'; 
import { getMeetingDetail, getMeetingStatus } from '../services/api';
import Navigation from "../components/Navigation";
import ResultView from "../components/ResultView";
import ProcessingIndicator from '../components/ProcessingIndicator';

const ResultPage = () => {
  const { id } = useParams(); 
  const [meeting, setMeeting] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!id) return;

    let pollInterval;

    const fetchData = async () => {
      try {
        const statusData = await getMeetingStatus(id);

        if (statusData.status === 'completed') {
          const details = await getMeetingDetail(id);
          setMeeting(details);
          setLoading(false);
          if (pollInterval) clearInterval(pollInterval);
        } else if (statusData.status === 'failed') {
          setError("AI extraction failed for this meeting.");
          setLoading(false);
          if (pollInterval) clearInterval(pollInterval);
        }
      } catch (err) {
        setError(err.message);
        setLoading(false);
        if (pollInterval) clearInterval(pollInterval);
      }
    };

    fetchData();
    pollInterval = setInterval(fetchData, 3000);

    return () => {
      if (pollInterval) clearInterval(pollInterval);
    };
  }, [id]);

  if (loading) return <ProcessingIndicator />;
  
  if (error) return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <div className="flex items-center justify-center pt-20 px-4">
        <div className="bg-red-50 border-l-4 border-red-500 p-6 rounded-md shadow-sm max-w-lg w-full">
          <h3 className="text-red-800 font-bold text-lg mb-2">Processing Error</h3>
          <p className="text-red-700">{error}</p>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
    
      <main className="container mx-auto pt-8 pb-16 max-w-5xl px-4 md:px-6">
        <ResultView meeting={meeting} />
      </main>
    </div>
  );
};

export default ResultPage;