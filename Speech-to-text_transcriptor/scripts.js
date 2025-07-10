const listenBtn = document.getElementById("listen-btn");
const copyBtn = document.getElementById("copy-btn");
const downloadBtn = document.getElementById("download-btn");
const transcriptDiv = document.getElementById("transcript");
const notification = document.getElementById("notification");
const aiRing = document.getElementById("aiRing");
const languageSelect = document.getElementById("language"); // ✅ FIXED: was missing

let isListening = false;
let recognition;
let finalTranscript = "";

// ✅ Check browser support
if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
  notification.textContent = "Your browser does not support Speech Recognition.";
  listenBtn.disabled = true;
} else {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();

  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = languageSelect.value;

  // Optional: Enhance microphone capture
  navigator.mediaDevices.getUserMedia({
    audio: {
      noiseSuppression: true,
      echoCancellation: true,
      sampleRate: 44100
    }
  }).catch(err => {
    console.warn("Microphone access error:", err);
  });

  recognition.onstart = () => {
    aiRing.classList.add("listening");
    listenBtn.textContent = "🛑 Stop Listening";
    notification.textContent = "";
  };

  recognition.onerror = (event) => {
    notification.textContent = "Error: " + event.error;
  };

  recognition.onend = () => {
    aiRing.classList.remove("listening");
    isListening = false;
    listenBtn.textContent = "🎤 Listen";
  };

  recognition.onresult = (event) => {
    let interim = "";
    for (let i = event.resultIndex; i < event.results.length; ++i) {
      let sentence = event.results[i][0].transcript.trim();

      // Capitalize first letter
      sentence = sentence.charAt(0).toUpperCase() + sentence.slice(1);

      // Add comma after common transition words
      const transitions = ["however", "therefore", "moreover", "meanwhile", "nonetheless", "furthermore", "instead"];
      transitions.forEach(word => {
        const regex = new RegExp(`\\b${word}\\b`, "gi");
        sentence = sentence.replace(regex, match => match.charAt(0).toUpperCase() + match.slice(1) + ",");
      });

      // Add period if missing
      if (!/[.?!]$/.test(sentence)) {
        sentence += ".";
      }

      if (event.results[i].isFinal) {
        finalTranscript += sentence + " ";
      } else {
        interim += sentence;
      }
    }

    transcriptDiv.textContent = finalTranscript + interim;

    const hasText = (finalTranscript + interim).trim().length > 0;
    copyBtn.disabled = !hasText;
    downloadBtn.disabled = !hasText;
  };
}

// 🎙️ Toggle Listening
listenBtn.onclick = () => {
  if (!isListening) {
    finalTranscript = "";
    transcriptDiv.textContent = "";
    recognition.lang = languageSelect.value; // ✅ Update lang on toggle
    recognition.start();
    isListening = true;
  } else {
    recognition.stop();
  }
};

// 📋 Copy Text
copyBtn.onclick = () => {
  navigator.clipboard.writeText(transcriptDiv.textContent);
  notification.textContent = "Copied!";
  setTimeout(() => (notification.textContent = ""), 1500);
};

// 💾 Download Text
downloadBtn.onclick = () => {
  const blob = new Blob([transcriptDiv.textContent], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "transcript.txt";
  a.click();
  URL.revokeObjectURL(url);
  notification.textContent = "Downloaded!";
  setTimeout(() => (notification.textContent = ""), 1500);
};
