# AI Speech-to-Text Transcription System

## Description
A real-time browser-based Speech-to-Text Transcription System built using JavaScript and the Web Speech API. It allows users to transcribe their speech live into written text, supports multiple languages and accents, includes automatic punctuation enhancements, and provides a minimal, futuristic UI with an animated AI ring indicator.

## Key Features
- 🎙️ Toggle listening on/off via a single button.
- 📜 Live transcription display with auto punctuation and capitalization.
- 🌐 Multi-language support (English, Hindi, Spanish, French, German, Japanese, Chinese).
- 🎧 Optimized audio input with noise suppression and echo cancellation.
- 📋 Copy to clipboard feature.
- 💾 Download transcript as `.txt`.
- 🔵 Animated AI ring indicating active listening.
- ⚙️ Responsive design with minimal controls over a custom animated background.

## Technologies Used
- HTML5
- CSS3 (Custom animated ring UI)
- Vanilla JavaScript
- Web Speech API (`SpeechRecognition` / `webkitSpeechRecognition`)
- Optional: MediaDevices API for enhanced mic input

## Setup Instructions
1. Clone or download the repository.
2. Open `index.html` in any modern browser (Chrome recommended).
3. Allow microphone access when prompted.
4. Click “🎤 Listen” to start real-time transcription.

## Future Enhancements
- Add theme toggle (dark/light).
- Integrate storage to save transcription history.
- Allow exporting as `.pdf` or `.docx`.
- Visual waveform feedback.

## Browser Support
✅ Chrome (Recommended)  
⚠️ Edge (Partial)  
❌ Firefox/Safari (SpeechRecognition not supported)

## Note
No external libraries or AI models are used—fully client-side and lightweight.
