const API = "http://localhost:8000"

export async function startTraining(courseId: string) {

  const res = await fetch(`${API}/coach/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ course_id: courseId })
  })

  return res.json()
}


export async function nextSlide() {

  const res = await fetch(`${API}/coach/next`, {
    method: "POST"
  })

  return res.json()
}


export async function askCoach(question: string) {

  const res = await fetch(`${API}/coach/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  })

  return res.json()
}

export async function fetchSlide(courseId: string, slide: number) {
  const res = await fetch(
    `${API}/courses/${courseId}/slides/${slide}`
  )

  if (!res.ok) throw new Error("Slide fetch failed")

  return res.json()
}

export async function uploadContent(
  courseId: string,
  file: File,
  transcript?: File
) {
  const formData = new FormData()

  formData.append("course_id", courseId)
  formData.append("file", file)

  if (transcript) {
    formData.append("transcript", transcript)
  }

  const res = await fetch(`${API}/content/upload`, {
    method: "POST",
    body: formData
  })

  if (!res.ok) {
    throw new Error("Upload failed")
  }

  return res.json()
}