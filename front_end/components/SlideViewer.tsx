"use client"

import { useEffect, useState } from "react"

import {
    connectCoach,
    startTraining,
    nextSlide,
    subscribe,
    resumeNarration,
    isSocketOpen
} from "../lib/coachRuntime"

import { speak, stopSpeech } from "../lib/speech"

interface Props {
    courseId: string
}

export default function SlideViewer({ courseId }: Props) {

    const [content, setContent] = useState("")
    const [slide, setSlide] = useState(0)

    useEffect(() => {

        connectCoach()

        const handler = (data: any) => {

            if (data.type === "slide") {

                stopSpeech()

                setSlide(data.slide)
                setContent(data.content)

                speak(data.content)

            }

            if (data.type === "answer") {

                stopSpeech()

                setContent(data.content)

                speak(data.content, () => {
                    speak("Do you have any other doubts?", () => {
                        speak("Resuming Explanation", () => {
                            if (isSocketOpen()) {
                                resumeNarration()
                            }
                        })
                    })


                })

            }

            if (data.type === "resume") {

                speak(data.content)

            }

            if (data.type === "stop_training") {

                stopSpeech()

                setContent(data.content)

                speak(data.content)

            }


            if (data.type === "training_complete") {

                alert("Training completed")

            }

        }

        subscribe(handler)

    }, [])

    function start() {

        if (!courseId) {
            alert("Please enter a course id")
            return
        }

        startTraining(courseId)

    }

    function next() {

        stopSpeech()

        nextSlide()

    }

    return (

        <div className="border rounded p-6 mb-6">

            <h2 className="text-xl font-semibold mb-4">
                Slide Viewer
            </h2>

            <p className="mb-3 text-gray-500">
                Slide {slide}
            </p>

            <div className="flex gap-3 mb-4">

                <button
                    onClick={start}
                    className="bg-green-600 text-white px-4 py-2 rounded"
                >
                    Give Explanation
                </button>

                <button
                    onClick={next}
                    className="bg-blue-600 text-white px-4 py-2 rounded"
                >
                    Next Slide
                </button>

            </div>

            <div className="whitespace-pre-wrap text-gray-700">
                {content}
            </div>

        </div>
    )
}