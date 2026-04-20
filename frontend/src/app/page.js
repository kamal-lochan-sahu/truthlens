"use client";
import { useState, useRef } from "react";

export default function Home() {
  const [mode, setMode] = useState("upload"); // "upload" or "link"
  const [url, setUrl] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const fileInputRef = useRef(null);

  // File select hone par preview dikhane ke liye
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
    }
  };

  // URL Mode (V1) Submit
  const analyzeLink = async (e) => {
    e.preventDefault();
    setLoading(true); setError(null); setResult(null);
    try {
      const response = await fetch("http://127.0.0.1:8000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url, image_url: imageUrl || null }),
      });
      const data = await response.json();
      if (!response.ok || !data.success) throw new Error(data.detail || data.error || "Analysis failed!");
      setResult(data.data);
    } catch (err) { setError(err.message); } 
    finally { setLoading(false); }
  };

  // Upload Mode (V2) Submit
  const analyzeUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select an image first!");
      return;
    }
    setLoading(true); setError(null); setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/analyze-upload", {
        method: "POST",
        // Fetch API apne aap Content-Type: multipart/form-data set kar lega
        body: formData,
      });
      const data = await response.json();
      if (!response.ok || !data.success) throw new Error(data.detail || data.error || "Analysis failed!");
      setResult(data.data);
    } catch (err) { setError(err.message); } 
    finally { setLoading(false); }
  };

  return (
    <main className="min-h-screen bg-gray-950 text-gray-100 p-8 font-sans selection:bg-purple-500/30">
      <div className="max-w-4xl mx-auto">
        
        {/* Header Section */}
        <div className="text-center mb-10 mt-6">
          <h1 className="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500 mb-4 tracking-tight">
            TruthLens <span className="text-purple-400">👁️</span>
          </h1>
          <p className="text-gray-400 text-lg">AI-Powered Deep Fake & Misinformation Detector</p>
        </div>

        {/* Mode Switcher */}
        <div className="flex justify-center space-x-4 mb-8">
          <button 
            onClick={() => {setMode("upload"); setResult(null); setError(null);}}
            className={`px-6 py-2 rounded-full font-semibold transition-all ${mode === "upload" ? "bg-purple-600 text-white shadow-lg shadow-purple-500/30" : "bg-gray-800 text-gray-400 hover:bg-gray-700"}`}
          >
            📸 Upload Image
          </button>
          <button 
            onClick={() => {setMode("link"); setResult(null); setError(null);}}
            className={`px-6 py-2 rounded-full font-semibold transition-all ${mode === "link" ? "bg-blue-600 text-white shadow-lg shadow-blue-500/30" : "bg-gray-800 text-gray-400 hover:bg-gray-700"}`}
          >
            🔗 Scan Web Link
          </button>
        </div>

        {/* Input Forms */}
        <div className="bg-gray-900/80 p-8 rounded-2xl border border-gray-800 mb-12 backdrop-blur-sm shadow-2xl">
          
          {/* UPLOAD MODE UI */}
          {mode === "upload" && (
            <form onSubmit={analyzeUpload} className="space-y-6">
              <div 
                className="border-2 border-dashed border-gray-700 hover:border-purple-500 rounded-xl p-8 text-center cursor-pointer transition-colors"
                onClick={() => fileInputRef.current.click()}
              >
                <input 
                  type="file" 
                  ref={fileInputRef} 
                  onChange={handleFileChange} 
                  accept="image/*" 
                  className="hidden" 
                />
                
                {preview ? (
                  <div className="space-y-4">
                    <img src={preview} alt="Preview" className="mx-auto max-h-64 rounded-lg shadow-md object-contain" />
                    <p className="text-purple-400 font-medium text-sm">Click to change image</p>
                  </div>
                ) : (
                  <div className="space-y-4 py-8">
                    <div className="text-6xl">📥</div>
                    <p className="text-gray-300 font-medium text-lg">Click to Upload a Screenshot or Image</p>
                    <p className="text-gray-500 text-sm">PNG, JPG, GIF accepted</p>
                  </div>
                )}
              </div>

              <button 
                type="submit" disabled={loading}
                className={`w-full py-4 rounded-xl font-bold text-lg transition-all ${loading ? "bg-gray-800 text-gray-500 cursor-not-allowed border border-gray-700" : "bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white shadow-lg hover:shadow-purple-500/25"}`}
              >
                {loading ? "🤖 Gemini is Extracting & Analyzing..." : "Scan Image for Truth"}
              </button>
            </form>
          )}

          {/* LINK MODE UI */}
          {mode === "link" && (
            <form onSubmit={analyzeLink} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">News Article URL (Required)</label>
                <input type="url" required value={url} onChange={(e) => setUrl(e.target.value)} placeholder="https://www.bbc.com/news/..." 
                  className="w-full px-4 py-3 bg-gray-950 border border-gray-800 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all text-gray-200" />
              </div>
              <button 
                type="submit" disabled={loading}
                className={`w-full py-4 rounded-xl font-bold text-lg transition-all ${loading ? "bg-gray-800 text-gray-500 cursor-not-allowed border border-gray-700" : "bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white shadow-lg hover:shadow-blue-500/25"}`}
              >
                {loading ? "🕵️ Scraping & Analyzing..." : "Scan Web Link"}
              </button>
            </form>
          )}
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-950/50 border border-red-500/50 text-red-200 p-4 rounded-xl mb-8 flex items-center space-x-3">
            <span className="text-xl">⚠️</span>
            <p>{error}</p>
          </div>
        )}

        {/* Results Section */}
        {result && (
          <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
            <h2 className="text-2xl font-bold border-b border-gray-800 pb-3 text-gray-200">Analysis Report</h2>
            
            {/* Extracted Text (Only for Upload Mode) */}
            {result.extracted_text && (
              <div className="bg-gray-900/80 p-6 rounded-xl border border-gray-800 shadow-lg">
                <h3 className="text-sm uppercase tracking-wider font-semibold mb-3 text-indigo-400 flex items-center"><span className="mr-2">📝</span> Text Extracted by AI</h3>
                <p className="text-gray-300 bg-gray-950 p-4 rounded-lg font-mono text-sm leading-relaxed border border-gray-800/50">
                  {result.extracted_text}
                </p>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Text Analysis Card */}
              <div className="bg-gray-900/80 p-6 rounded-xl border border-gray-800 shadow-lg">
                <h3 className="text-lg font-semibold mb-4 text-purple-400 flex items-center"><span className="mr-2">🧠</span> AI Text Analysis</h3>
                <div className="flex items-center justify-between bg-gray-950 p-4 rounded-lg mb-3">
                  <span className="text-gray-400">Verdict</span>
                  <span className={`px-4 py-1.5 rounded-full text-sm font-bold tracking-wide ${result.text_analysis.label === 'Real' ? 'bg-green-500/10 text-green-400 border border-green-500/20' : 'bg-red-500/10 text-red-400 border border-red-500/20'}`}>
                    {result.text_analysis.label.toUpperCase()}
                  </span>
                </div>
                <div className="flex items-center justify-between px-2">
                  <span className="text-gray-500 text-sm">Confidence</span>
                  <span className="font-mono text-gray-300">{result.text_analysis.confidence}%</span>
                </div>
              </div>

              {/* Fact Check Card */}
              <div className="bg-gray-900/80 p-6 rounded-xl border border-gray-800 shadow-lg">
                <h3 className="text-lg font-semibold mb-4 text-blue-400 flex items-center"><span className="mr-2">🔍</span> Google Fact-Check</h3>
                {result.fact_check.fact_found ? (
                  <div className="space-y-3">
                    <div className="bg-gray-950 p-3 rounded-lg border border-gray-800/50">
                      <p className="text-xs text-gray-500 mb-1 uppercase tracking-wider">Claim Investigated</p>
                      <p className="text-sm text-gray-300 italic">"{result.fact_check.claim}"</p>
                    </div>
                    <div className="flex items-center justify-between px-2 pt-2">
                      <span className="text-gray-500 text-sm">Reviewer</span>
                      <span className="text-blue-300 text-sm">{result.fact_check.reviewer}</span>
                    </div>
                    <div className="flex items-center justify-between px-2">
                      <span className="text-gray-500 text-sm">Official Verdict</span>
                      <span className="font-bold text-red-400 uppercase tracking-wide">{result.fact_check.verdict}</span>
                    </div>
                  </div>
                ) : (
                  <div className="h-full flex flex-col items-center justify-center text-center p-4">
                    <span className="text-4xl mb-3 opacity-50">🤷‍♂️</span>
                    <p className="text-gray-400 text-sm leading-relaxed">No specific fact-checks found matching this exact text in Google's database.</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}