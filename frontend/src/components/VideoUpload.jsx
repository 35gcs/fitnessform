import React, { useState, useRef } from 'react'
import axios from 'axios'
import './VideoUpload.css'

function VideoUpload({ onAnalysisComplete, onAnalysisStart }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [exerciseType, setExerciseType] = useState('squat')
  const [previewUrl, setPreviewUrl] = useState(null)
  const [error, setError] = useState(null)
  const fileInputRef = useRef(null)

  const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
      if (!file.type.startsWith('video/')) {
        setError('Please select a video file')
        return
      }

      if (file.size > 100 * 1024 * 1024) { // 100MB limit
        setError('File size must be less than 100MB')
        return
      }

      setSelectedFile(file)
      setPreviewUrl(URL.createObjectURL(file))
      setError(null)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a video file first')
      return
    }

    onAnalysisStart()

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const endpoint = exerciseType === 'squat'
        ? '/api/analyze/squat'
        : '/api/analyze/deadlift'

      const response = await axios.post(endpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      onAnalysisComplete(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.')
      onAnalysisComplete(null)
    }
  }

  const handleDrop = (event) => {
    event.preventDefault()
    const file = event.dataTransfer.files[0]
    if (file) {
      handleFileSelect({ target: { files: [file] } })
    }
  }

  const handleDragOver = (event) => {
    event.preventDefault()
  }

  return (
    <div className="video-upload">
      <div className="upload-card">
        <h2>Upload Your Weightlifting Video</h2>
        <p className="subtitle">Get instant form analysis and corrective exercises</p>

        <div className="exercise-selector">
          <label>Select Exercise:</label>
          <div className="exercise-buttons">
            <button
              className={exerciseType === 'squat' ? 'active' : ''}
              onClick={() => setExerciseType('squat')}
            >
              Squat
            </button>
            <button
              className={exerciseType === 'deadlift' ? 'active' : ''}
              onClick={() => setExerciseType('deadlift')}
            >
              Deadlift
            </button>
          </div>
        </div>

        <div
          className="drop-zone"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onClick={() => fileInputRef.current?.click()}
        >
          {previewUrl ? (
            <div className="preview">
              <video src={previewUrl} controls className="preview-video" />
              <p className="file-name">{selectedFile?.name}</p>
            </div>
          ) : (
            <div className="drop-zone-content">
              <svg
                className="upload-icon"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                />
              </svg>
              <p className="drop-text">Drop your video here or click to browse</p>
              <p className="file-info">Supports MP4, MOV, AVI (Max 100MB)</p>
            </div>
          )}
          <input
            ref={fileInputRef}
            type="file"
            accept="video/*"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <button
          className="analyze-button"
          onClick={handleUpload}
          disabled={!selectedFile}
        >
          Analyze My Form
        </button>

        <div className="tips">
          <h3>Tips for Best Results:</h3>
          <ul>
            <li>Film from the side view (sagittal plane)</li>
            <li>Ensure your full body is visible throughout the movement</li>
            <li>Use good lighting and avoid shadows</li>
            <li>Perform 1-3 reps for analysis</li>
            <li>Keep the camera steady</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default VideoUpload
