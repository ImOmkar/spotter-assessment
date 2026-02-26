const ROWS = [
    { key: "off_duty", label: "Off Duty", color: "bg-gray-500" },
    { key: "sleeper", label: "Sleeper", color: "bg-purple-500" },
    { key: "driving", label: "Driving", color: "bg-green-500" },
    { key: "on_duty", label: "On Duty", color: "bg-orange-500" },
  ];

  const ON_DUTY_TYPES = [
    "on_duty",
    "pickup",
    "fuel",
    "dropoff",
    "break",
  ];
  
  export default function ELDGrid({ log, onHoverSegment  }) {
    return (
    <div className="bg-white rounded-xl shadow-sm border p-6 overflow-hidden">
  
        {/* Header */}
        <div className="flex justify-between mb-6">
          <h3 className="font-semibold text-lg">
            Day {log.day}
          </h3>
  
          <div className="text-sm text-gray-600">
            Driving <b>{log.driving_hours}h</b> |
            On Duty <b>{log.on_duty_hours}h</b>
          </div>
        </div>
  
        {/* Timeline Wrapper */}
        <div className="overflow-x-auto scrollbar-thin scrollbar-thumb-gray-300">
            <div className="min-w-[1400px]">
  
                {/* Empty spacer */}
                <div />
        
                {/* Time ruler */}
                <div className="grid grid-cols-24 text-[11px] text-gray-400 mb-3">
                    {[...Array(24)].map((_, i) => (
                    <div key={i} className="text-center">
                        {i}
                    </div>
                    ))}
                </div>
        
                {/* MASTER GRID */}
                <div />
                <div className="relative">
        
                    <div className="absolute inset-0 grid grid-cols-24 pointer-events-none">
                    {[...Array(24)].map((_, i) => (
                        <div key={i} className="border-l border-gray-200" />
                    ))}
                    </div>
        
                    {ROWS.map((row) => (
                    <div
                        key={row.key}
                        className="grid grid-cols-[120px_1fr] items-center h-14 border-t"
                    >
                        {/* Label column */}
                        <div className="text-sm font-medium text-gray-700">
                        {row.label}
                        </div>
        
                        {/* Timeline lane */}
                        <div className="relative h-10">
        
                        {log.timeline
                            .filter(e => {
                                if (row.key === "on_duty") {
                                return ON_DUTY_TYPES.includes(e.status);
                                }
                                return e.status === row.key;
                            })
                            .map((event, index) => {
        
                            const left = (event.start / 24) * 100;
                            const width =
                                ((event.end - event.start) / 24) * 100;
        
                            return (
                                <div
                                key={index}
                                title={`${event.status.toUpperCase()}
                                    ${event.start.toFixed(2)} → ${event.end.toFixed(2)} hrs`}
                                    onMouseEnter={() =>
                                        onHoverSegment({
                                        day: log.day,
                                        start: event.start,
                                        end: event.end,
                                        status: event.status,
                                        })
                                    }
                                    onMouseLeave={() => onHoverSegment(null)}
                                className={`${row.color}
                                    absolute
                                    top-1/2
                                    -translate-y-1/2
                                    h-6
                                    rounded`}
                                style={{
                                    left: `${left}%`,
                                    width: `${width}%`,
                                }}
                                />
                            );
                            })}
                        </div>
                    </div>
                    ))}
                </div>
                </div>
            </div>
      </div>
    );
  }