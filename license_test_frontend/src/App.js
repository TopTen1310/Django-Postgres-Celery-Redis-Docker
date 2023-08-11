import Home from './pages/Home'
import { NotificationContainer } from 'react-notifications'
import { Routes, Route } from 'react-router-dom'

function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
      <NotificationContainer />
    </div>
  )
}

export default App
