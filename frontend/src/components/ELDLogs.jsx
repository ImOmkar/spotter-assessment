import ELDGrid from "./ELDGrid";

export default function ELDLogs({ logs, onHoverSegment  }) {
    return (
      <div className="h-full w-full overflow-y-auto bg-gray-100 p-4 space-y-5">
        {logs.map((log) => (
          <ELDGrid key={log.day} log={log} onHoverSegment={onHoverSegment} />
        ))}
      </div>
    );
  }