import { Link, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";

const Navigation = () => {
  const location = useLocation();

  return (
    <nav className="border-b bg-white sticky top-0 z-50">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-6">
          <Link to="/" className="text-xl font-bold text-blue-600">
            Meeting Assistant
          </Link>
          <div className="flex gap-4">
            <Link 
              to="/" 
              className={`text-sm font-medium ${location.pathname === '/' ? 'text-blue-600' : 'text-gray-500'}`}
            >
              New Meeting
            </Link>
            <Link 
              to="/history" 
              className={`text-sm font-medium ${location.pathname === '/history' ? 'text-blue-600' : 'text-gray-500'}`}
            >
              History
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;