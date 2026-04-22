import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Navigation from "../components/Navigation";
import ResultView from "../components/ResultView";
import ProcessingIndicator from "../components/ProcessingIndicator";
import { getMeetingDetail } from "../services/api";

const MeetingDetailPage = () => {
  const { id } = useParams();
  const [meeting, setMeeting] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDetail = async () => {
      try {
        const data = await getMeetingDetail(id);
        setMeeting(data);
      } catch (err) { console.error(err); }
      setLoading(false);
    };
    fetchDetail();
  }, [id]);

  if (loading) return <ProcessingIndicator />;

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <main className="container py-10 max-w-5xl">
        <div className="mb-8">
          <h1 className="text-4xl font-extrabold">{meeting?.title}</h1>
          <p className="text-muted-foreground">{meeting?.meeting_date}</p>
        </div>
        {meeting && <ResultView meeting={meeting} />}
      </main>
    </div>
  );
};

export default MeetingDetailPage;