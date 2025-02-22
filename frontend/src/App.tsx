import { HashRouter, Route, Routes } from "react-router-dom";
import Lobby from "./Lobby";
import Account from "./Account";
import Tutorial from "./Tutorial";
import AgentTraining from "./AgentTraining";

function App() {
  return (
    <HashRouter>
      <div>
        {/* Main Content */}
        <main style={{ padding: "20px" }}>
          <Routes>
            <Route path="/" element={<Lobby />} />
            <Route path="/account" element={<Account />} />
            <Route path="/tutorial" element={<Tutorial />} />
            <Route path="/agentTraining" element={<AgentTraining />} />
          </Routes>
        </main>
      </div>
    </HashRouter>
  );
}

export default App;
