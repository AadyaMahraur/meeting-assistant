import {Routes, Route} from 'react-router-dom';
import HistoryPage from './pages/HistoryPage';
import HomePage from './pages/HomePage';
import MeetingDetailPage from './pages/MeetingDetailPage';
import ResultPage from './pages/ResultPage';


function App() {
  

  return (
    <>
      <Routes>
        <Route path='/' element={<HomePage/>} />
        <Route path='/history' element={<HistoryPage/>} />
        {/* make the routes below dynamic */}
        <Route path='/meetingDetails' element={<MeetingDetailPage/>} /> 
        <Route path='/results' element={<ResultPage/>} /> 
      </Routes>
    </>
    
  )
}

export default App
