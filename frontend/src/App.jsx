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
        <Route path='/meeting/:id' element={<MeetingDetailPage/>} />
        <Route path='/results/:id' element={<ResultPage/>} /> 
      </Routes>
    </>
    
  )
}

export default App
