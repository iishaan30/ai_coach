"use client"

import { useState } from "react"
import { uploadContent } from "../lib/api"

export default function ContentUploader() {

  const [courseId, setCourseId] = useState("")
  const [file, setFile] = useState<File | null>(null)
  const [transcript, setTranscript] = useState<File | null>(null)
  const [status, setStatus] = useState("")

  async function handleUpload() {

    if (!courseId || !file) {
      alert("Course ID and file required")
      return
    }

    try {

      setStatus("Uploading...")

      await uploadContent(courseId, file, transcript || undefined)

      setStatus("Upload successful! Ingestion started.")

    } catch (err) {

      console.error(err)
      setStatus("Upload failed")

    }
  }

  return (
    <div className="border rounded p-6 mb-6">

      <h2 className="text-xl font-semibold mb-4">
        Upload Training Content
      </h2>

      <input
        className="border p-2 w-full mb-3"
        placeholder="Course ID"
        value={courseId}
        onChange={(e) => setCourseId(e.target.value)}
      />

      <input
        type="file"
        accept=".pdf,.ppt,.pptx"
        className="mb-3"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <input
        type="file"
        accept=".txt"
        className="mb-3"
        onChange={(e) => setTranscript(e.target.files?.[0] || null)}
      />

      <button
        onClick={handleUpload}
        className="bg-purple-600 text-white px-4 py-2 rounded"
      >
        Upload Content
      </button>

      {status && (
        <p className="mt-3 text-sm text-gray-600">{status}</p>
      )}

    </div>
  )
}