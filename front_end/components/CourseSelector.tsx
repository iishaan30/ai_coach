"use client"

interface Props {
  courseId: string
  setCourseId: (id: string) => void
}

export default function CourseSelector({ courseId, setCourseId }: Props) {
  return (
    <div className="mb-6">
      <label className="block text-sm font-semibold">
        Course ID
      </label>

      <input
        value={courseId}
        onChange={(e) => setCourseId(e.target.value)}
        className="border p-2 rounded w-full"
        placeholder="test-course-1"
      />
    </div>
  )
}