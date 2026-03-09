"use client"

import { useState, useRef } from "react"

import { askQuestion, sendAudio } from "../lib/coachRuntime"
import { stopSpeech } from "../lib/speech"

let asking = false

export default function CoachChat() {

const [question,setQuestion] = useState("")
const [recording,setRecording] = useState(false)

const mediaRecorderRef = useRef<MediaRecorder | null>(null)
const audioChunksRef = useRef<Blob[]>([])

function sendQuestion(q:string){


if(!q || asking) return

asking = true

stopSpeech()

askQuestion(q)

setTimeout(()=>{
  asking = false
},1500)


}

function ask(){


if(!question) return

sendQuestion(question)

setQuestion("")


}

async function startVoice(){


stopSpeech()

const stream = await navigator.mediaDevices.getUserMedia({audio:true})

const mediaRecorder = new MediaRecorder(stream)

mediaRecorderRef.current = mediaRecorder

audioChunksRef.current = []

mediaRecorder.ondataavailable = (event)=>{
  audioChunksRef.current.push(event.data)
}

mediaRecorder.onstop = async ()=>{

  const blob = new Blob(audioChunksRef.current,{type:"audio/webm"})

  sendAudio(blob)

  setRecording(false)

}

mediaRecorder.start()

setRecording(true)


}

function stopVoice(){


if(mediaRecorderRef.current){

  mediaRecorderRef.current.stop()

}


}

return (


<div className="border rounded p-6">

  <h2 className="text-xl font-semibold mb-4">
    Ask the Coach
  </h2>

  <textarea
    value={question}
    onChange={(e)=>setQuestion(e.target.value)}
    className="border p-3 w-full mb-3"
    placeholder="Ask a question..."
  />

  <div className="flex gap-3">

    <button
      onClick={ask}
      className="bg-green-600 text-white px-4 py-2 rounded"
    >
      Ask
    </button>

    {!recording && (

      <button
        onClick={startVoice}
        className="bg-purple-600 text-white px-4 py-2 rounded"
      >
        🎤 Start Speaking
      </button>

    )}

    {recording && (

      <button
        onClick={stopVoice}
        className="bg-red-600 text-white px-4 py-2 rounded"
      >
        ⏹ Stop Recording
      </button>

    )}

  </div>

  {recording && (
    <p className="mt-3 text-purple-500">
      Recording...
    </p>
  )}

</div>


)
}
