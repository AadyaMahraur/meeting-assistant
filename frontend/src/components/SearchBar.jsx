import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { Search, Loader2 } from "lucide-react";

const SearchBar = ({ onSearch, isLoading }) => {
  const [value, setValue] = useState("");

  useEffect(() => {
    if (value === "") return;
    const timer = setTimeout(() => {
      onSearch(value);
    }, 500); // Wait 500ms after last keystroke

    return () => clearTimeout(timer);
  }, [value]);

  return (
    <div className="relative w-full max-w-sm">
      <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
        {isLoading ? (
          <Loader2 className="h-4 w-4 animate-spin" />
        ) : (
          <Search className="h-4 w-4" />
        )}
      </div>
      <Input
        type="text"
        placeholder="Search title, actions, or decisions..."
        className="pl-10"
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
    </div>
  );
};

export default SearchBar;