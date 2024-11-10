import React, { useState } from "react";
import axios from "axios";

function App() {
  const [prompt, setPrompt] = useState(""); // State for the current prompt input
  const [chatHistory, setChatHistory] = useState([]); // State to store chat history
  const [loading, setLoading] = useState(false); // Loading state

  // Function to handle prompt submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post("http://localhost:8000/ask/", {
        prompt: prompt,
      });

      // Update chat history with the new prompt and response
      setChatHistory([
        { prompt: prompt, response: response.data.response },
        ...chatHistory, // Display latest interactions at the top
      ]);

      setPrompt(""); // Clear the prompt input
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      {/* Header */}
      <header className="bg-pms202 text-white text-xl font-semibold p-4 text-center">
        Chat with Mohit
      </header>

      {/* Chat History */}
      <div className="flex-grow p-4 overflow-y-auto">
        {chatHistory.length === 0 ? (
          <p className="text-gray-500 text-center mt-4">
            No previous responses. Start the conversation!
          </p>
        ) : (
          chatHistory.map((entry, index) => (
            <div key={index} className="mb-4">
              <div className="bg-gray-200 rounded-lg p-3">
                <strong>Prompt:</strong> {entry.prompt}
              </div>
              <div className="bg-blue-100 rounded-lg p-3 mt-2">
                <strong>Response:</strong> {entry.response}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Prompt Input */}
      <form
        onSubmit={handleSubmit}
        className="p-4 bg-white border-t border-gray-300 flex items-center space-x-2 sticky bottom-0"
      >
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your prompt..."
          required
          className="flex-grow p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          disabled={loading}
          className={`px-4 py-2 rounded-lg font-semibold text-white ${
            loading ? "bg-pms202" : "bg-pms202 hover:bg-red-700"
          }`}
        >
          {loading ? "Loading..." : "Enter"}
        </button>
      </form>
    </div>
  );
}

export default App;
