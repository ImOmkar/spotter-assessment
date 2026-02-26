import { useState } from "react";
import { planTrip } from "../api/tripApi";
import MapView from "../components/MapView";
import TripPanel from "../components/TripPanel";
import ELDLogs from "../components/ELDLogs";
import TripSummary from "../components/TripSummary";
import LoadingOverlay from "../components/LoadingOverlay";
import Remarks from "../components/Remarks";

export default function Dashboard() {

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showLogs, setShowLogs] = useState(false);
  const [hoverSegment, setHoverSegment] = useState(null);

  const handlePlanTrip = async (tripData) => {
    try {
      setLoading(true);
  
      const result = await planTrip(tripData);
  
      setData(result);
      setShowLogs(true);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };


return (
    <div className="h-screen flex flex-col overflow-hidden">
  
      {loading && <LoadingOverlay />}
  
      {/* ================= MAIN AREA ================= */}
      <div className="flex flex-1 min-h-0 overflow-hidden">
  
        {/* LEFT PANEL */}
        <div className="w-80 border-r flex flex-col overflow-y-auto bg-white">
          {data && (
            <div className="p-4 border-b">
              <TripSummary
                route={data.route}
                hos={data.hos}
              />
              <Remarks remarks={data.hos.remarks} />
            </div>
          )}
  
          <TripPanel onPlan={handlePlanTrip} />
        </div>
  
        {/* MAP AREA */}
        <div className="flex-1 relative min-h-0">
          {data && (
            <MapView
              route={data.route}
              stops={data.stops}
              layoutTrigger={showLogs}
            />
          )}
        </div>
      </div>
  
      {/* ================= LOG PANEL ================= */}
      {data && (
        <div
          className={`
            transition-all duration-300 border-t bg-gray-100
            ${showLogs ? "h-[340px]" : "h-10"}
          `}
        >
          {/* Toggle */}
          <div className="bg-white py-2 flex justify-center border-b">
            <button
              onClick={() => setShowLogs(!showLogs)}
              className="text-sm font-medium text-blue-600"
            >
              {showLogs ? "Hide ELD Logs ↓" : "Show ELD Logs ↑"}
            </button>
          </div>
  
          {/* Logs */}
          {showLogs && (
            <div className="h-[300px] overflow-auto">
              <ELDLogs logs={data.hos.logs} />
            </div>
          )}
        </div>
      )}
  
    </div>
  );
}