export default function LoadingOverlay() {
    return (
      <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-[999]">
        
        <div className="bg-white rounded-xl p-6 shadow-xl flex items-center gap-4">
          
          <div className="animate-spin rounded-full h-8 w-8 border-4 border-blue-500 border-t-transparent"></div>
  
          <div>
            <p className="font-semibold text-gray-800">
              Planning Trip...
            </p>
            <p className="text-sm text-gray-500">
              Calculating route & ELD compliance
            </p>
          </div>
  
        </div>
  
      </div>
    )
  }