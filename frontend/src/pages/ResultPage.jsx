import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { getMeetingDetail, getMeetingStatus } from '../services/api';
import ProcessingIndicator from '../components/ProcessingIndicator';
import ActionItemsTable from '../components/ActionItemsTable';
import DecisionsList from '../components/DecisionsList';
import BlockersList from '../components/BlockersList';
import EmailDraftView from '../components/EmailDraftView';

const ResultPage = () => {
  const [searchParams] = useSearchParams();
  const meetingId = searchParams.get('id');
  
  const [meeting, setMeeting] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!meetingId) return;

    let pollInterval;

    const fetchData = async () => {
      try {
        // 1. Check status first
        const statusData = await getMeetingStatus(meetingId);

        if (statusData.status === 'completed') {
          // 2. If finished, get full details and stop polling
          const details = await getMeetingDetail(meetingId);
          setMeeting(details);
          setLoading(false);
          clearInterval(pollInterval);
        } else if (statusData.status === 'failed') {
          setError("AI extraction failed for this meeting.");
          setLoading(false);
          clearInterval(pollInterval);
        }
        // If 'pending', we do nothing and let the interval run again
      } catch (err) {
        setError(err.message);
        setLoading(false);
        clearInterval(pollInterval);
      }
    };

    // Initial fetch
    fetchData();

    // Start polling every 3 seconds
    pollInterval = setInterval(fetchData, 3000);

    return () => clearInterval(pollInterval);
  }, [meetingId]);

  if (loading) return <ProcessingIndicator />;
  if (error) return <div className="p-10 text-red-600">Error: {error}</div>;

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-8">
      {/* Header */}
      <header className="border-b pb-4">
        <h1 className="text-3xl font-bold text-gray-900">{meeting.title}</h1>
        <p className="text-gray-500">{meeting.meeting_date}</p>
      </header>

      {/* Short Summary Box */}
      <section className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded shadow-sm">
        <h2 className="text-lg font-semibold text-blue-800 mb-1">Executive Summary</h2>
        <p className="text-blue-900 italic">"{meeting.short_summary}"</p>
      </section>

      {/* Detailed Summary */}
      <section>
        <h2 className="text-xl font-bold mb-2">Detailed Overview</h2>
        <p className="text-gray-700 leading-relaxed">{meeting.detailed_summary}</p>
      </section>

      {/* Grid for Actions and Decisions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <ActionItemsTable items={meeting.action_items} />
        <DecisionsList items={meeting.decisions} />
      </div>

      <BlockersList items={meeting.blockers} />
      
      <EmailDraftView text={meeting.followup_email} />
    </div>
  );
};

export default ResultPage;