import { HashRouter, Route, Routes } from "react-router-dom";
import Lobby from "./pages/Lobby";
import Tutorial from "./pages/Tutorial";
import AgentTraining from "./pages/AgentTraining";
import AgentSetUp from "./pages/AgentSetUp";

function App() {
  return (
    <HashRouter>
      <div>
        {/* Main Content */}
        <main style={{ padding: "10px" }}>
          <Routes>
            <Route path="/" element={<Lobby />} />
            <Route path="/tutorial" element={<Tutorial />} />
            <Route path="/agentTraining" element={<AgentTraining />} />
            <Route path="/agentSetUp" element={<AgentSetUp />} />
          </Routes>
        </main>
      </div>
    </HashRouter>
  );
}

export default App;
