import { useEffect, useState, useCallback } from "react";
import { getAllMeetings, searchMeetings } from "@/services/api"; // Added searchMeetings
import Navigation from "../components/Navigation";
import MeetingCard from "../components/MeetingCard";
import SearchBar from "../components/SearchBar"; // Don't forget to import this
import { Button } from "@/components/ui/button";

const HistoryPage = () => {
  // 1. All States must be inside the component
  const [data, setData] = useState({ meetings: [], total: 0 });
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [isSearching, setIsSearching] = useState(false);

  // 2. Define the load logic
  const loadData = useCallback(async () => {
    console.log(`Fetching: Search="${searchTerm}", Page=${page}`);
    setLoading(true);
    try {
      let result;
      // If there is text in the search bar, use the search API
      if (searchTerm.trim()) {
        setIsSearching(true);
        result = await searchMeetings(searchTerm, page);
      } else {
        // Otherwise, use the standard history API
        setIsSearching(false);
        result = await getAllMeetings(page);
      }
      setData(result);
    } catch (err) {
      console.error("Data load error:", err);
    } finally {
      setLoading(false);
    }
  }, [searchTerm, page]); // Triggers whenever search text or page changes

  // 3. One single useEffect to rule them all
  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleSearch = useCallback((val) => {
    setSearchTerm((prev) => {
      // ONLY reset to page 1 if the search text actually changed
      if (prev !== val) {
        setPage(1);
        return val;
      }
      return prev;
    });
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <main className="container py-10">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <h1 className="text-3xl font-bold">Meeting History</h1>
          {/* 5. Add the SearchBar component */}
          <SearchBar onSearch={handleSearch} isLoading={loading && isSearching} />
        </div>
        
        {loading && data.meetings.length === 0 ? (
          <div className="flex justify-center py-20">Processing...</div>
        ) : data.meetings.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {data.meetings.map(m => <MeetingCard key={m.id} meeting={m} />)}
          </div>
        ) : (
          <div className="text-center py-20 bg-white rounded-lg border-2 border-dashed">
            <p className="text-muted-foreground">No meetings found.</p>
          </div>
        )}

        {/* 6. Pagination - Only show if we have results and not currently searching (or adjust as needed) */}
        {data.total > 0 && (
          <div className="flex justify-center items-center mt-10 gap-4">
            <Button 
              variant="outline" 
              disabled={page === 1 || loading} 
              onClick={() => setPage(p => p - 1)}
            >Previous</Button>
            
            <span className="text-sm text-muted-foreground">
              Page {page}
            </span>

            <Button 
              variant="outline" 
              disabled={page * 9 >= data.total || loading} 
              onClick={() => setPage(p => p + 1)}
            >Next</Button>
          </div>
        )}
      </main>
    </div>
  );
};

export default HistoryPage;