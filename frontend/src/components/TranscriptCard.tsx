import React from 'react';

export interface Transcript {
    id: number;
    original_text: string;
    summary_text: string | null;
    created_at: string; // Assuming ISO string format from backend
    updated_at: string; // Assuming ISO string format from backend
  }

interface TranscriptCardProps {
    transcript: Transcript;
    onRerunSummary: (id: number) => void; // Callback when 'Re-run Summary' is clicked
    onShowCommLog: (id: number) => void;   // Callback when 'Show CommLog' is clicked (currently not rendered)
  }
  
const TranscriptCard: React.FC<TranscriptCardProps> = ({ transcript, onRerunSummary, onShowCommLog }) => {
  const handleRerunClick = () => {
    onRerunSummary(transcript.id);
  };

  // const handleShowCommLogClick = () => {
  //   onShowCommLog(transcript.id);
  // };

  return (
    <div className="bg-gray-800 p-4 sm:p-5 rounded-lg shadow-lg hover:shadow-indigo-500/30 transition-all duration-300 ease-in-out">
      {/* Card Header: ID and Action Button(s) */}
      <div className="flex flex-col sm:flex-row justify-between sm:items-center mb-3 sm:mb-4">
        <h2 className="text-lg sm:text-xl font-semibold text-blue-400 mb-2 sm:mb-0">
          Transcript ID: {transcript.id}
        </h2>
        <div className="flex space-x-2">
          <button
            onClick={handleRerunClick}
            className="text-xs bg-indigo-500 hover:bg-indigo-600 focus:ring-2 focus:ring-indigo-400 focus:ring-opacity-50 text-white py-1.5 px-3 rounded-md transition-colors duration-200 ease-in-out whitespace-nowrap shadow hover:shadow-md"
            aria-label={`Re-run summary for transcript ${transcript.id}`}
          >
            Re-run Summary
          </button>
          {/* 
          Placeholder for Show CommLog button. Uncomment and style if you add this feature.
          <button
            onClick={handleShowCommLogClick}
            className="text-xs bg-gray-600 hover:bg-gray-500 focus:ring-2 focus:ring-gray-400 focus:ring-opacity-50 text-white py-1.5 px-3 rounded-md transition-colors duration-200 ease-in-out whitespace-nowrap shadow hover:shadow-md"
            aria-label={`Show communication log for transcript ${transcript.id}`}
          >
            Show CommLog
          </button>
          */}
        </div>
      </div>

      {/* Original Text Section */}
      <div className="mb-4">
        <h3 className="text-sm font-medium text-gray-300 mb-1">Original Text:</h3>
        <div className="bg-gray-700/70 p-3 rounded-md max-h-36 overflow-y-auto custom-scrollbar">
          <p className="text-sm text-gray-400 whitespace-pre-wrap break-words">
            {transcript.original_text}
          </p>
        </div>
      </div>

      {/* Summary Text Section */}
      <div className="mb-4">
        <h3 className="text-sm font-medium text-gray-300 mb-1">Summary:</h3>
        <div className={`p-3 rounded-md ${transcript.summary_text ? 'bg-green-700/30' : 'bg-yellow-700/30'}`}>
          {transcript.summary_text ? (
            <p className="text-sm text-green-300 whitespace-pre-wrap break-words">
              {transcript.summary_text}
            </p>
          ) : (
            <p className="text-sm text-yellow-300 animate-pulse">
              Summary pending...
            </p>
          )}
        </div>
      </div>

      {/* Timestamps Footer */}
      <div className="text-xs text-gray-500 mt-auto pt-3 border-t border-gray-700/50 flex flex-col sm:flex-row justify-between items-center gap-1 sm:gap-2">
        <span>
          Created: {new Date(transcript.created_at).toLocaleString()}
        </span>
        <span>
          Updated: {new Date(transcript.updated_at).toLocaleString()}
        </span>
      </div>
    </div>
  );
};

export default TranscriptCard;
  
