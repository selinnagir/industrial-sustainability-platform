import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom"
import AppShell from "./components/layout/AppShell"
import DashboardPage from "./pages/DashboardPage"
import CarbonPage from "./pages/CarbonPage"
import UploadCenterPage from "./pages/UploadCenterPage"
import CompanyDashboardPage from "./pages/CompanyDashboardPage"
import AIAnalysisPage from "./pages/AIAnalysisPage"
import AIChatboxPage from "./pages/AIChatboxPage"
import ScenarioSimulationPage from "./pages/ScenarioSimulationPage"
import BenchmarkPage from "./pages/BenchmarkPage"

export default function App() {
  return (
    <BrowserRouter>
      <AppShell>
        <Routes>
          <Route path="/" element={<Navigate to="/reference-dashboard" replace />} />
          <Route path="/reference-dashboard" element={<DashboardPage />} />
          <Route path="/carbon" element={<CarbonPage />} />
          <Route path="/upload-center" element={<UploadCenterPage />} />
          <Route path="/company-dashboard" element={<CompanyDashboardPage />} />
          <Route path="/ai-analysis" element={<AIAnalysisPage />} />
          <Route path="/ai-chatbox" element={<AIChatboxPage />} />
          <Route path="/scenario-simulation" element={<ScenarioSimulationPage />} />
          <Route path="/benchmark" element={<BenchmarkPage />} />
        </Routes>
      </AppShell>
    </BrowserRouter>
  )
}
