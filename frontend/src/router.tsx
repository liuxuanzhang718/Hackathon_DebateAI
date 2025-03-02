import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Lobby from './pages/Lobby';
import AgentTraining from './pages/AgentTraining';
import Tutorial from './pages/Tutorial';
// import Account from './Account';

function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/lobby" element={<Lobby />} />
        <Route path="/agent-training" element={<AgentTraining />} />
        <Route path="/tutorial" element={<Tutorial />} />
        {/* <Route path="/account" element={<Account />} /> */}
      </Routes>
    </Router>
  );
}

export default AppRouter;
