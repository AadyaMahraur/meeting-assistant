import { Link, useLocation } from "react-router-dom";

const Navigation = () => {
  const location = useLocation();

  return (
    <nav className="border-b bg-white sticky top-0 z-50">
      <div className="container px-4 md:px-8 flex h-16 items-center justify-between max-w-7xl">
        <div className="flex items-center gap-6 md:gap-10">
          <Link to="/" className="text-xl font-bold text-blue-600 tracking-tight">
            Meeting Assistant
          </Link>
          <div className="flex gap-6">
            <Link 
              to="/" 
              className={`text-sm font-medium transition-colors ${location.pathname === '/' ? 'text-blue-600' : 'text-gray-500 hover:text-gray-900'}`}
            >
              New Meeting
            </Link>
            <Link 
              to="/history" 
              className={`text-sm font-medium transition-colors ${location.pathname === '/history' ? 'text-blue-600' : 'text-gray-500 hover:text-gray-900'}`}
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