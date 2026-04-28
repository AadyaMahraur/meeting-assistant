import { useEffect, useState, useCallback } from "react";
import { getAllMeetings, searchMeetings } from "@/services/api"; 
import Navigation from "../components/Navigation";
import MeetingCard from "../components/MeetingCard";
import SearchBar from "../components/SearchBar"; 
import { Button } from "@/components/ui/button";

const HistoryPage = () => {
  const [data, setData] = useState({ meetings: [], total: 0 });
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [isSearching, setIsSearching] = useState(false);

  const loadData = useCallback(async () => {
    console.log(`Fetching: Search="${searchTerm}", Page=${page}`);
    setLoading(true);
    try {
      let result;
      if (searchTerm.trim()) {
        setIsSearching(true);
        result = await searchMeetings(searchTerm, page);
      } else {
        setIsSearching(false);
        result = await getAllMeetings(page);
      }
      setData(result);
    } catch (err) {
      console.error("Data load error:", err);
    } finally {
      setLoading(false);
    }
  }, [searchTerm, page]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleSearch = useCallback((val) => {
    setSearchTerm(val);
    setPage(1); 
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      
      <main className="container mx-auto pt-8 pb-16 px-4 md:px-8 max-w-7xl">
        
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <h1 className="text-3xl font-bold text-gray-900">Meeting History</h1>
          <SearchBar onSearch={handleSearch} isLoading={loading && isSearching} />
        </div>
        
        {loading && data.meetings.length === 0 ? (
          <div className="flex justify-center py-20 text-gray-600 font-medium">Processing...</div>
        ) : data.meetings.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {data.meetings.map(m => <MeetingCard key={m.id} meeting={m} />)}
          </div>
        ) : (
          <div className="text-center py-20 bg-white rounded-xl border-2 border-dashed border-gray-200">
            <p className="text-gray-500 font-medium">No meetings found.</p>
          </div>
        )}

        {data.total > 0 && (
          <div className="flex justify-center items-center mt-12 gap-4">
            <Button 
              variant="outline" 
              disabled={page === 1 || loading} 
              onClick={() => setPage(p => p - 1)}
              className="shadow-sm"
            >
              Previous
            </Button>
            
            <span className="text-sm font-medium text-gray-500">
              Page {page}
            </span>

            <Button 
              variant="outline" 
              disabled={page * 9 >= data.total || loading} 
              onClick={() => setPage(p => p + 1)}
              className="shadow-sm"
            >
              Next
            </Button>
          </div>
        )}
      </main>
    </div>
  );
};

export default HistoryPage;