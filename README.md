# 🎙️ PodCast AI - PDF to Audio Learning

Transform your PDF documents into engaging student-teacher podcast conversations with AI-powered natural voices.

![PodCast AI](https://img.shields.io/badge/Powered%20by-Groq%20AI-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/License-MIT-purple)

## ✨ Features

- **📄 PDF Processing**: Upload any PDF document and extract its content
- **🤖 AI Script Generation**: Uses Groq's LLaMA 3.3 70B to create natural conversations
- **🎧 Text-to-Speech**: Converts the script to audio with distinct voices for teacher and student
- **💫 Premium UI**: Beautiful, modern interface with animations and glassmorphism design
- **📥 Download Audio**: Get your podcast as an MP3 file

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- FFmpeg (required for audio processing)

### Installation

1. **Install FFmpeg** (if not already installed):
   
   **Windows (via Chocolatey):**
   ```bash
   choco install ffmpeg
   ```
   
   **Windows (Manual):**
   - Download from https://ffmpeg.org/download.html
   - Add to your system PATH

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   Navigate to `http://localhost:5000`

## 🎯 How It Works

1. **Upload PDF**: Drag and drop or click to upload your PDF document
2. **Preview Content**: Review the extracted text from your PDF
3. **Generate Script**: AI creates an engaging student-teacher conversation
4. **Create Audio**: Each dialogue is converted to speech with natural voices
5. **Listen & Download**: Play your podcast or download the MP3 file

## 🔧 Configuration

The application uses these environment variables (set in `.env`):

```env
GROQ_API_KEY=your_groq_api_key_here
```

## 📁 Project Structure

```
new_cast/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── templates/
│   └── index.html     # Main HTML template
├── static/
│   ├── style.css      # Premium CSS styles
│   └── script.js      # Frontend JavaScript
├── uploads/           # Uploaded PDF files
└── outputs/           # Generated audio files
```

## 🎨 Features in Detail

### AI-Powered Conversations
The AI creates natural dialogues between:
- **Teacher** 👨‍🏫: Experienced, patient, uses analogies and examples
- **Student** 👨‍🎓: Curious, asks thoughtful questions

### Premium Audio
- High-quality text-to-speech using Groq's TTS API
- Distinct voices for each speaker
- Natural pacing with pauses between dialogues

### Beautiful UI
- Glassmorphism design
- Animated backgrounds
- Responsive layout
- Progress indicators
- Audio visualization

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application page |
| `/api/upload` | POST | Upload PDF file |
| `/api/generate-script` | POST | Generate podcast script |
| `/api/generate-audio` | POST | Create audio from script |
| `/api/download/<filename>` | GET | Download audio file |
| `/api/stream/<filename>` | GET | Stream audio file |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Groq](https://groq.com) for the blazing fast AI inference
- [PyPDF2](https://pypdf2.readthedocs.io/) for PDF processing
- [Pydub](https://pydub.com/) for audio manipulation
- [Flask](https://flask.palletsprojects.com/) for the web framework

---

Made with ❤️ for learners who prefer listening over reading!
