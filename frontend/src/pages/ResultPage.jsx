import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom'; // Changed from useSearchParams
import { getMeetingDetail, getMeetingStatus } from '../services/api';
import Navigation from "../components/Navigation";
import ResultView from "../components/ResultView";
import ProcessingIndicator from '../components/ProcessingIndicator';

const ResultPage = () => {
  const { id } = useParams(); // Now matches /results/:id
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
  if (error) return <div className="p-10 text-red-600">Error: {error}</div>;

  return (
  <div>
    <Navigation />
    {loading ? <Spinner /> : <ResultView meeting={meeting} />}
  </div>
  );
};

export default ResultPage;