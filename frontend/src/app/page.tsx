"use client";

import { useEffect, useState } from 'react';
import TranscriptCard, { Transcript as ExternalTranscriptInterface } from '@/components/TranscriptCard';

type PageTranscript = ExternalTranscriptInterface;

// Define an interface for CommLog entries (should match your backend schema)
interface CommLogEntry {
  id: number;
  event_type: string;
  details: string | null;
  transcript_id: number | null;
  timestamp: string;
}

const API_BASE_URL = 'http://localhost:8000/api/v1';

export default function DashboardPage() {
  const [transcripts, setTranscripts] = useState<PageTranscript[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newTranscriptText, setNewTranscriptText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // --- New state for CommLog ---
  const [commlogTranscriptId, setCommlogTranscriptId] = useState<string>(''); // For the input field
  const [commlogEntries, setCommlogEntries] = useState<CommLogEntry[]>([]);
  const [isCommlogLoading, setIsCommlogLoading] = useState(false);
  const [commlogError, setCommlogError] = useState<string | null>(null);
  // --- End New state for CommLog ---

  const fetchTranscripts = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/transcripts/?limit=50&skip=0`);
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: response.statusText }));
        throw new Error(`Error ${response.status}: ${errorData.detail || response.statusText}`);
      }
      const data: PageTranscript[] = await response.json();
      setTranscripts(data);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred while fetching transcripts.");
      }
      console.error("Failed to fetch transcripts:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTranscripts();
  }, []);

  const handleRerunSummary = async (id: number) => {
    console.log("Attempting to re-run summary for transcript ID:", id);
    alert(`Placeholder: Re-run summary for ID ${id}. This needs a backend endpoint.`);
    
  };

  const handleShowCommLog = (id: number) => {
    console.log("Attempting to show commlog for transcript ID:", id);
    // TODO: Implement fetching and displaying commlog, perhaps in a modal
    alert(`Placeholder: Show CommLog for ID ${id}.`);
  };

  const handleSubmitNewTranscript = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!newTranscriptText.trim()) {
      alert("Transcript text cannot be empty.");
      return;
    }
    setIsSubmitting(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/transcripts/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ original_text: newTranscriptText }),
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: response.statusText }));
        throw new Error(`Error ${response.status}: ${errorData.detail || response.statusText}`);
      }
      setNewTranscriptText('');
      await fetchTranscripts();
      console.log("New transcript submitted successfully");
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred while submitting transcript.");
      }
      console.error("Failed to submit transcript:", err);
    } finally {
      setIsSubmitting(false);
    }
  };

  // --- Function to fetch CommLog for a specific Transcript ID ---
  const handleFetchCommlog = async (e?: React.FormEvent<HTMLFormElement>) => {
    if (e) e.preventDefault(); // Prevent form submission if called from form
    if (!commlogTranscriptId.trim()) {
      setCommlogError("Please enter a Transcript ID.");
      setCommlogEntries([]);
      return;
    }

    const id = parseInt(commlogTranscriptId, 10);
    if (isNaN(id)) {
      setCommlogError("Invalid Transcript ID. Must be a number.");
      setCommlogEntries([]);
      return;
    }

    setIsCommlogLoading(true);
    setCommlogError(null);
    setCommlogEntries([]); // Clear previous logs

    try {
      const response = await fetch(`${API_BASE_URL}/commlogs/transcript/${id}`);
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error(`No transcript or logs found for ID: ${id}`);
        }
        const errorData = await response.json().catch(() => ({ detail: response.statusText }));
        throw new Error(`Error ${response.status}: ${errorData.detail || response.statusText}`);
      }
      const data: CommLogEntry[] = await response.json();
      setCommlogEntries(data);
      if (data.length === 0) {
        // Optionally set a message if no logs found for an existing transcript
        setCommlogError(`No communication logs found for Transcript ID: ${id}.`);
      }
    } catch (err) {
      if (err instanceof Error) {
        setCommlogError(err.message);
      } else {
        setCommlogError("An unknown error occurred while fetching commlogs.");
      }
      console.error("Failed to fetch commlogs:", err);
    } finally {
      setIsCommlogLoading(false);
    }
  };

  // --- Loading and Error States (Main Page Level) ---
  if (isLoading && transcripts.length === 0) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-12 bg-gray-900 text-white font-sans">
        <p className="text-xl">Loading AI Call Summaries...</p>
        <svg className="animate-spin h-8 w-8 text-blue-400 mt-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </main>
    );
  }
  // --- End Loading and Error States ---

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col p-4 md:p-6 font-sans">
      <header className="mb-6 py-4">
        <h1 className="text-4xl font-bold text-center text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-500">
          AI Call Summary Dashboard
        </h1>
      </header>

      {error && (
         <div className="mb-4 p-4 bg-red-800/50 border border-red-700 text-red-300 rounded-md">
           <p><strong>Error:</strong> {error}</p>
           <button 
             onClick={fetchTranscripts} 
             className="mt-2 bg-red-500 hover:bg-red-600 text-white py-1 px-3 rounded text-sm"
           >
             Retry Fetch
           </button>
         </div>
       )}

      <div className="flex flex-1 flex-col md:flex-row gap-6">
        {/* Left Column: Transcripts List */}
        <section className="md:w-2/3 flex flex-col">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-semibold text-gray-300">Recent Transcripts</h2>
            <button 
              onClick={fetchTranscripts}
              disabled={isLoading && transcripts.length > 0} // Disable only if refreshing
              className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-md transition-colors text-sm disabled:opacity-50"
            >
              {(isLoading && transcripts.length > 0) ? 'Refreshing...' : 'Refresh List'}
            </button>
          </div>
          
          {(!isLoading && transcripts.length === 0 && !error) ? (
            <div className="flex-1 flex items-center justify-center bg-gray-800 p-6 rounded-lg shadow-lg">
              <p className="text-gray-400">No transcripts found. Submit one using the form!</p>
            </div>
          ) : (
            <div className="flex-1 space-y-4 overflow-y-auto max-h-[calc(100vh-15rem)] pr-2 custom-scrollbar">
              {transcripts.map((transcript) => (
                <TranscriptCard 
                  key={transcript.id} 
                  transcript={transcript}
                  onRerunSummary={handleRerunSummary} // Pass the defined handler
                  onShowCommLog={handleShowCommLog}   // Pass the defined handler
                />
              ))}
            </div>
          )}
        </section>

        {/* Right Column: Form Box and CommLog Display */}
        <aside className="md:w-1/3 bg-gray-800 p-6 rounded-lg shadow-lg h-fit sticky top-6 space-y-8">
          {/* Submit New Transcript Form */}
          <div>
            <h2 className="text-2xl font-semibold mb-4 text-gray-300">Submit New Transcript</h2>
            <form onSubmit={handleSubmitNewTranscript}>
              <div className="mb-4">
                <label htmlFor="transcriptText" className="block text-sm font-medium text-gray-400 mb-1">
                  Call Transcript Text:
                </label>
                <textarea
                  id="transcriptText"
                  name="transcriptText"
                  rows={8}
                  className="w-full p-3 bg-gray-700 border border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-200 placeholder-gray-500 custom-scrollbar"
                  placeholder="Paste the call transcript here..."
                  value={newTranscriptText}
                  onChange={(e) => setNewTranscriptText(e.target.value)}
                  disabled={isSubmitting}
                />
              </div>
              <button
                type="submit"
                disabled={isSubmitting || !newTranscriptText.trim()}
                className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-2.5 px-4 rounded-md transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? 'Submitting...' : 'Submit & Summarize'}
              </button>
            </form>
          </div>

          {/* Divider */}
          <hr className="border-gray-700" />

          {/* View CommLog Section */}
          <div>
            <h2 className="text-2xl font-semibold mb-4 text-gray-300">View Communication Log</h2>
            <form onSubmit={handleFetchCommlog} className="flex items-end gap-3 mb-4">
              <div className="flex-grow">
                <label htmlFor="commlogTranscriptId" className="block text-sm font-medium text-gray-400 mb-1">
                  Enter Transcript ID:
                </label>
                <input
                  type="number"
                  id="commlogTranscriptId"
                  name="commlogTranscriptId"
                  className="w-full p-2.5 bg-gray-700 border border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-200 placeholder-gray-500"
                  placeholder="e.g., 123"
                  value={commlogTranscriptId}
                  onChange={(e) => setCommlogTranscriptId(e.target.value)}
                  disabled={isCommlogLoading}
                />
              </div>
              <button
                type="submit"
                disabled={isCommlogLoading || !commlogTranscriptId.trim()}
                className="bg-cyan-600 hover:bg-cyan-700 text-white font-semibold py-2.5 px-4 rounded-md transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
              >
                {isCommlogLoading ? 'Loading...' : 'View Logs'}
              </button>
            </form>

            {/* CommLog Display Area Box - MODIFIED for consistent height */}
            <div className="mt-4 min-h-[12rem] max-h-96 bg-gray-700/30 p-3 rounded-md custom-scrollbar overflow-y-auto flex flex-col"> {/* Added min-h, adjusted max-h, added flex for centering content */}
              {isCommlogLoading ? (
                <div className="flex-grow flex items-center justify-center"> {/* Centering wrapper */}
                  <p className="text-sm text-gray-400">Loading logs...</p>
                  {/* Optionally, add a small spinner here */}
                </div>
              ) : commlogError ? (
                <div className="flex-grow flex items-center justify-center"> {/* Centering wrapper */}
                  <p className="text-sm text-red-400 text-center">{commlogError}</p>
                </div>
              ) : commlogEntries.length > 0 ? (
                <div className="space-y-3"> {/* Container for actual log entries */}
                  {commlogEntries.map((log) => (
                    <div key={log.id} className="bg-gray-700/50 p-3 rounded-md shadow">
                      <p className="text-xs text-purple-300 font-semibold">{log.event_type}</p>
                      {log.details && <p className="text-xs text-gray-400 mt-1 break-words">{log.details}</p>}
                      <p className="text-xs text-gray-500 mt-1">
                        {new Date(log.timestamp).toLocaleString()}
                      </p>
                    </div>
                  ))}
                </div>
              ) : commlogTranscriptId && !commlogError ? ( // Searched, but no entries
                <div className="flex-grow flex items-center justify-center"> {/* Centering wrapper */}
                  <p className="text-sm text-gray-500">No communication logs found for Transcript ID: {commlogTranscriptId}.</p>
                </div>
              ) : ( // Default state before any search, or if ID input is cleared
                <div className="flex-grow flex items-center justify-center"> {/* Centering wrapper */}
                  <p className="text-sm text-gray-500">Enter a Transcript ID to view logs.</p>
                </div>
              )}
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}