import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom"; // <-- Added useNavigate here
import Navigation from "../components/Navigation";
import ResultView from "../components/ResultView";
import ProcessingIndicator from "../components/ProcessingIndicator";
import { getMeetingDetail, deleteMeeting } from "../services/api";

const MeetingDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [meeting, setMeeting] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDetail = async () => {
      try {
        const data = await getMeetingDetail(id);
        setMeeting(data);
      } catch (err) { 
        console.error("Error fetching meeting:", err); 
      } finally {
        setLoading(false);
      }
    };
    fetchDetail();
  }, [id]);

  const handleDelete = async () => {
      const isConfirmed = window.confirm("Are you sure you want to delete this meeting? This cannot be undone.");
      
      if (isConfirmed) {
          try {
              await deleteMeeting(id); 
              navigate('/'); 
          } catch (error) {
              console.error("Error deleting meeting:", error);
              alert("Failed to delete the meeting. Please try again.");
          }
      }
  };

  if (loading) return <ProcessingIndicator />;

  if (!meeting) return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <h2 className="text-2xl font-bold text-gray-600">Meeting not found.</h2>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <main className="container mx-auto py-10 max-w-5xl px-4">
        
        <div className="mb-8 flex justify-between items-start">
          <div>
            <h1 className="text-4xl font-extrabold text-gray-900">{meeting.title}</h1>
            <p className="text-gray-500 mt-2">Date: {meeting.meeting_date}</p>
          </div>
          
          <button 
              onClick={handleDelete}
              className="bg-red-500 hover:bg-red-600 transition-colors text-white font-bold py-2 px-6 rounded shadow-sm"
          >
              Delete Meeting
          </button>
        </div>

        <ResultView meeting={meeting} />
      </main>
    </div>
  );
};

export default MeetingDetailPage;