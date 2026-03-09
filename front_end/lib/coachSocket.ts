let socket: WebSocket | null = null

export function connectCoach(onMessage:any){

  if(socket) return   // ⭐ prevents second connection

  socket = new WebSocket("ws://localhost:8000/ws/coach")

  socket.onopen = () => {
    console.log("Coach WebSocket connected")
  }

  socket.onmessage = (event)=>{

    const data = JSON.parse(event.data)

    onMessage(data)

  }

}

export function askQuestion(question:string){

  if(!socket) return

  socket.send(JSON.stringify({
    type: "question",
    question
  }))

}

export function nextSlide(){

  if(!socket) return

  socket.send(JSON.stringify({
    type: "next"
  }))

}