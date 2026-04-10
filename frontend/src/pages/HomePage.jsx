import NavBar from '../components/Navigation.jsx'
import { useState, useEffect } from 'react';
import apiClient from '../services/api.js';



function HomePage() {
    const [connectionStatus, setConnectionStatus] = useState('Checking connection...');

  useEffect(() => {
    // Call the health endpoint
    apiClient.get('/health')
      .then((response) => {
        if (response.data.status === 'healthy') {
          setConnectionStatus('Backend connected');
        }
      })
      .catch((error) => {
        console.error("Health check failed:", error);
        setConnectionStatus('Backend not available');
      });
  }, []);
  return (
    <>
        
        <h1>Home Page</h1>
        <NavBar/>
        <div className="status-badge">
            <p>Status: <strong>{connectionStatus}</strong></p>
        </div>
    </> 
  )
}

export default HomePage