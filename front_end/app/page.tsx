"use client"

import { useState } from "react"
import CourseSelector from "../components/CourseSelector"
import SlideViewer from "../components/SlideViewer"
import CoachChat from "../components/CoachChat"
import ContentUploader from "@/components/ContentUploader"

export default function Home() {
  const [courseId, setCourseId] = useState("")

  return (
    <main className="max-w-4xl mx-auto p-10">

      <h1 className="text-3xl font-bold mb-8">
        Virtual AI Training Coach
      </h1>

      <ContentUploader/>

      <CourseSelector
        courseId={courseId}
        setCourseId={setCourseId}
      />

      <SlideViewer courseId={courseId} />

      <CoachChat />

    </main>
  )
}