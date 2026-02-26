export default function TripSummary({ route, hos }) {

    if (!route || !hos) return null;
  
    const remainingCycle =
      70 - hos.summary.final_cycle_hours;
  
    return (
      <div className="bg-white shadow-lg rounded-lg p-4 space-y-3">
  
        <h2 className="text-lg font-semibold">
          Trip Summary
        </h2>
  
        <div className="grid grid-cols-2 gap-3 text-sm">
  
          <SummaryItem
            label="Distance"
            value={`${route.distance_miles} mi`}
          />
  
          <SummaryItem
            label="Drive Time"
            value={`${route.duration_hours} hrs`}
          />
  
          <SummaryItem
            label="Trip Days"
            value={hos.summary.total_days}
          />
  
          <SummaryItem
            label="Cycle Used"
            value={`${hos.summary.final_cycle_hours} / 70 hrs`}
          />
  
          <SummaryItem
            label="Cycle Remaining"
            value={`${remainingCycle.toFixed(1)} hrs`}
          />
  
          <SummaryItem
            label="Estimated Finish"
            value={`Day ${hos.summary.total_days}`}
          />
  
        </div>
  
      </div>
    );
  }
  
  
  function SummaryItem({ label, value }) {
    return (
      <div className="bg-gray-50 rounded p-3">
        <p className="text-gray-500 text-xs">
          {label}
        </p>
        <p className="font-semibold">
          {value}
        </p>
      </div>
    );
  }