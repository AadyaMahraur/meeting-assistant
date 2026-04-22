import { getAllMeetings } from "@/services/api";
import { useEffect, useState } from "react";
import Navigation from "../components/Navigation";
import MeetingCard from "../components/MeetingCard";
import { Button } from "@/components/ui/button";

const HistoryPage = () => {
  const [data, setData] = useState({ meetings: [], total: 0 });
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      setLoading(true);
      try {
        const result = await getAllMeetings(page);
        console.log(result);
        setData(result);
      } catch (err) { console.error(err); }
      setLoading(false);
    };
    fetchHistory();
  }, [page]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <main className="container py-10">
        <h1 className="text-3xl font-bold mb-8">Meeting History</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {data.meetings.map(m => <MeetingCard key={m.id} meeting={m} />)}
        </div>

        {/* Pagination */}
        <div className="flex justify-center mt-10 gap-2">
          <Button 
            variant="outline" 
            disabled={page === 1} 
            onClick={() => setPage(p => p - 1)}
          >Previous</Button>
          <Button 
            variant="outline" 
            disabled={page * 10 >= data.total} 
            onClick={() => setPage(p => p + 1)}
          >Next</Button>
        </div>
      </main>
    </div>
  );
};

export default HistoryPage;