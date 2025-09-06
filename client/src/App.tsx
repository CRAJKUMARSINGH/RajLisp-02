import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { ThemeProvider } from "@/components/theme-provider";
import Layout from "@/components/layout/Layout";
import Dashboard from "@/pages/Dashboard";
import BeamDesign from "@/pages/BeamDesign";
import ColumnDesign from "@/pages/ColumnDesign";
import FootingDesign from "@/pages/FootingDesign";
import RoadDesign from "@/pages/RoadDesign";
import StaircaseDesign from "@/pages/StaircaseDesign";
import BridgeDesign from "@/pages/BridgeDesign";
import LintelDesign from "@/pages/LintelDesign";
import SunshadeDesign from "@/pages/SunshadeDesign";
import DrawingCanvas from "@/pages/DrawingCanvas";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider defaultTheme="light" storageKey="rajlisp-theme">
        <TooltipProvider>
          <Router>
            <Layout>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/beams" element={<BeamDesign />} />
                <Route path="/columns" element={<ColumnDesign />} />
                <Route path="/footings" element={<FootingDesign />} />
                <Route path="/roads" element={<RoadDesign />} />
                <Route path="/staircases" element={<StaircaseDesign />} />
                <Route path="/bridges" element={<BridgeDesign />} />
                <Route path="/lintels" element={<LintelDesign />} />
                <Route path="/sunshades" element={<SunshadeDesign />} />
                <Route path="/canvas" element={<DrawingCanvas />} />
              </Routes>
            </Layout>
            <Toaster />
          </Router>
        </TooltipProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
