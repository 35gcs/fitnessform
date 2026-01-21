import React, { useState } from 'react'
import './App.css'
import VideoUpload from './components/VideoUpload'
import AnalysisResults from './components/AnalysisResults'

function App() {
  const [analysisResult, setAnalysisResult] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const handleAnalysisComplete = (result) => {
    setAnalysisResult(result)
    setIsAnalyzing(false)
  }

  const handleAnalysisStart = () => {
    setIsAnalyzing(true)
    setAnalysisResult(null)
  }

  const handleReset = () => {
    setAnalysisResult(null)
    setIsAnalyzing(false)
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>FitnessForm</h1>
        <p>AI-Powered Weightlifting Form Analyzer</p>
      </header>

      <main className="App-main">
        {!analysisResult && !isAnalyzing && (
          <VideoUpload
            onAnalysisComplete={handleAnalysisComplete}
            onAnalysisStart={handleAnalysisStart}
          />
        )}

        {isAnalyzing && (
          <div className="analyzing">
            <div className="spinner"></div>
            <h2>Analyzing your form...</h2>
            <p>This may take a moment while we process your video</p>
          </div>
        )}

        {analysisResult && (
          <AnalysisResults
            result={analysisResult}
            onReset={handleReset}
          />
        )}
      </main>

      <footer className="App-footer">
        <p>Focus on squats and deadlifts. Upload your video for expert form analysis.</p>
      </footer>
    </div>
  )
}

export default App
