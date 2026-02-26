export default function Remarks({ remarks }) {
    return (
      <div className="bg-white border rounded-lg p-4">
        <h3 className="font-semibold mb-3">
          Driver Remarks
        </h3>
  
        <div className="space-y-2 text-sm">
          {remarks.map((r, i) => (
            <div key={i}>
              Day {r.day} — {r.event} at {r.time}h
            </div>
          ))}
        </div>
      </div>
    );
  }