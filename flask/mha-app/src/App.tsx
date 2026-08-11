import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';


import Signup from './components/Signup';
import Login from './components/Login';
import ForgotPassword from './components/ForgotPassword';
import ResetPassword from './components/ResetPassword';
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password/:token" element={<ResetPassword />} />
      </Routes>
    </Router>
  );
}

export default App;
