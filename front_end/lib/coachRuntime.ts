let socket: WebSocket | null = null

type Listener = (data:any) => void

const listeners: Listener[] = []

export function subscribe(listener: Listener) {
  listeners.push(listener)
}

function notify(data:any) {
  listeners.forEach(l => l(data))
}

export function connectCoach() {

  if(socket && socket.readyState === WebSocket.OPEN) {
    return
  }

  socket = new WebSocket("ws://localhost:8000/ws/coach")

  socket.onopen = () => {
    console.log("Coach connected")
  }

  socket.onmessage = (event) => {

    const data = JSON.parse(event.data)

    notify(data)

  }

  socket.onclose = () => {
    console.log("Coach socket closed")
    socket = null
  }

  socket.onerror = (err) => {
    console.error("Socket error", err)
  }
}

export function startTraining(courseId:string){

  socket?.send(JSON.stringify({
    type: "start_training",
    course_id: courseId
  }))

}

export function askQuestion(question:string){

  socket?.send(JSON.stringify({
    type: "question",
    question
  }))

}

export function nextSlide(){

  socket?.send(JSON.stringify({
    type: "next"
  }))

}

export function resumeNarration(){

  socket?.send(JSON.stringify({
    type: "resume"
  }))

}

export function isSocketOpen(){
  return socket && socket.readyState === WebSocket.OPEN
}

export function sendAudio(blob: Blob) {

  if(socket && socket.readyState === WebSocket.OPEN){

    socket.send(blob)

  }

}