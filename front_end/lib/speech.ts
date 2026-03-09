export function speak(text: string, onEnd?: () => void) {

  const utterance = new SpeechSynthesisUtterance(text)

  utterance.rate = 1
  utterance.pitch = 1

  utterance.onend = () => {
    if (onEnd) onEnd()
  }

  window.speechSynthesis.speak(utterance)

}

export function stopSpeech() {
  window.speechSynthesis.cancel()
}