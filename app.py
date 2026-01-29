"""
PDF to Podcast Generator
Converts PDF content into engaging student-teacher conversations with audio
"""

import os
import json
import tempfile
from pathlib import Path
from flask import Flask, request, jsonify, send_file, render_template, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from groq import Groq
import PyPDF2
import base64

# Load environment variables from .env file
load_dotenv()

# Get API key
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Initialize Groq client lazily
_client = None

def get_groq_client():
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client

# Available voices for TTS (Edge-TTS Neural Voices)
LANGUAGE_VOICES = {
    "en": {
        "teacher": "en-US-GuyNeural",      # Male
        "student": "en-US-JennyNeural"     # Female
    },
    "hi": {
        "teacher": "hi-IN-MadhurNeural",   # Male
        "student": "hi-IN-SwaraNeural"     # Female
    },
    "es": {
        "teacher": "es-MX-JorgeNeural",    # Male
        "student": "es-MX-DaliaNeural"     # Female
    },
    "fr": {
        "teacher": "fr-FR-HenriNeural",    # Male
        "student": "fr-FR-DeniseNeural"    # Female
    },
    "de": {
        "teacher": "de-DE-ConradNeural",   # Male
        "student": "de-DE-KatjaNeural"     # Female
    }
}

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text content from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        raise Exception(f"Error extracting PDF text: {str(e)}")
    return text.strip()


def generate_podcast_script(pdf_content: str, language: str = "en") -> dict:
    """Generate a student-teacher conversation script from PDF content using Groq."""
    
    # Map language codes to full names for the prompt
    lang_names = {
        "en": "English",
        "hi": "Hindi",
        "es": "Spanish",
        "fr": "French",
        "de": "German"
    }
    target_language = lang_names.get(language, "English")
    
    system_prompt = f"""You are an expert educational podcast scriptwriter. Your task is to convert educational content into an engaging, natural conversation between a TEACHER (experienced, knowledgeable, patient) and a STUDENT (curious, asking good questions, seeking clarification).

Guidelines:
1. Make the conversation NATURAL and ENGAGING - like a real tutoring session
2. The teacher should explain concepts clearly using analogies and examples
3. The student should ask thoughtful questions and show genuine curiosity
4. Include moments of humor and relatability
5. Break down complex topics into digestible explanations
6. The conversation should flow naturally, not feel scripted
7. Include about 8-12 exchanges between teacher and student
8. Each response should be 1-3 sentences for natural speech rhythm
9. STRICTLY output the conversation in {target_language} language.

Output your response as a valid JSON object with this exact structure:
{{
    "title": "Podcast episode title",
    "summary": "Brief 2-3 sentence summary of what this episode covers",
    "conversation": [
        {{"speaker": "teacher", "text": "dialogue here..."}},
        {{"speaker": "student", "text": "dialogue here..."}},
        ...
    ]
}}

IMPORTANT: Return ONLY the JSON object, no other text."""

    user_prompt = f"""Convert the following educational content into an engaging student-teacher podcast conversation in {target_language}:

---
{pdf_content[:12000]}  
---

Remember to make it natural, educational, and engaging. Output only valid JSON in {target_language}."""

    try:
        completion = get_groq_client().chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        response_text = completion.choices[0].message.content.strip()
        
        # Try to parse the JSON response
        # Handle potential JSON wrapped in markdown code blocks
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1])
        if response_text.startswith("json"):
            response_text = response_text[4:]
            
        script = json.loads(response_text)
        return script
        
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse script JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"Error generating script: {str(e)}")


import asyncio
import edge_tts

async def generate_audio_async(text: str, voice: str, output_file: str):
    """Generate audio using Edge TTS asynchronously."""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

def generate_audio_for_dialogue(text: str, speaker: str, output_file: str, language: str = "en") -> str:
    """Generate audio for a single dialogue using Edge TTS."""
    
    # Get voices for the specified language, default to English if not found
    lang_voices = LANGUAGE_VOICES.get(language, LANGUAGE_VOICES["en"])
    voice = lang_voices.get(speaker, lang_voices["teacher"])
    
    try:
        # Run the async function
        asyncio.run(generate_audio_async(text, voice, output_file))
        return output_file
        
    except Exception as e:
        raise Exception(f"Error generating audio: {str(e)}")


def generate_full_podcast(script: dict, output_path: str, language: str = "en") -> str:
    """Generate the full podcast audio from the script."""
    
    from pydub import AudioSegment
    import tempfile
    import os as os_module
    
    conversation = script.get("conversation", [])
    if not conversation:
        raise Exception("No conversation found in script")
    
    # Initialize empty audio
    full_audio = AudioSegment.silent(duration=500)  # Start with 0.5s silence
    
    # Create temp directory for individual audio files
    temp_dir = tempfile.mkdtemp()
    
    for i, dialogue in enumerate(conversation):
        speaker = dialogue.get("speaker", "teacher")
        text = dialogue.get("text", "")
        
        if not text:
            continue
            
        print(f"Generating audio for {speaker}: {text[:50]}...")
        
        try:
            # Generate audio for this dialogue to a temp file
            temp_file = os_module.path.join(temp_dir, f"dialogue_{i}.mp3")
            generate_audio_for_dialogue(text, speaker, temp_file, language)
            
            # Load the audio file
            audio_segment = AudioSegment.from_mp3(temp_file)
            
            # Add a small pause between speakers
            pause = AudioSegment.silent(duration=400)  # 0.4s pause
            
            full_audio = full_audio + audio_segment + pause
            
            # Clean up temp file
            os_module.remove(temp_file)
            
        except Exception as e:
            print(f"Warning: Failed to generate audio for dialogue {i}: {str(e)}")
            continue
    
    # Clean up temp directory
    try:
        os_module.rmdir(temp_dir)
    except:
        pass
    
    # Add ending silence
    full_audio = full_audio + AudioSegment.silent(duration=1000)
    
    # Export the final audio
    full_audio.export(output_path, format="mp3", bitrate="192k")
    
    return output_path


@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_pdf():
    """Handle PDF upload and start processing."""
    
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF file provided"}), 400
    
    file = request.files['pdf']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400
    
    try:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(filepath)
        
        if not pdf_text or len(pdf_text) < 100:
            return jsonify({"error": "Could not extract sufficient text from PDF"}), 400
        
        return jsonify({
            "success": True,
            "message": "PDF uploaded successfully",
            "filename": filename,
            "text_length": len(pdf_text),
            "preview": pdf_text[:500] + "..." if len(pdf_text) > 500 else pdf_text
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/generate-script', methods=['POST'])
def generate_script():
    """Generate the podcast script from uploaded PDF."""
    
    data = request.json
    filename = data.get('filename')
    language = data.get('language', 'en')
    
    if not filename:
        return jsonify({"error": "No filename provided"}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    
    try:
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(filepath)
        
        # Generate the script
        script = generate_podcast_script(pdf_text, language)
        
        return jsonify({
            "success": True,
            "script": script
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/generate-audio', methods=['POST'])
def generate_audio():
    """Generate audio from the podcast script."""
    
    data = request.json
    script = data.get('script')
    filename = data.get('filename', 'podcast')
    language = data.get('language', 'en')
    
    if not script:
        return jsonify({"error": "No script provided"}), 400
    
    try:
        # Generate output filename
        output_filename = f"{Path(filename).stem}_podcast.mp3"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Generate the full podcast audio
        generate_full_podcast(script, output_path, language)
        
        return jsonify({
            "success": True,
            "audio_file": output_filename
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/download/<filename>')
def download_audio(filename):
    """Download the generated audio file."""
    try:
        return send_from_directory(
            app.config['OUTPUT_FOLDER'],
            filename,
            as_attachment=True,
            mimetype='audio/mpeg'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route('/api/stream/<filename>')
def stream_audio(filename):
    """Stream the generated audio file."""
    try:
        return send_from_directory(
            app.config['OUTPUT_FOLDER'],
            filename,
            mimetype='audio/mpeg'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 404


if __name__ == '__main__':
    print("🎙️ PDF to Podcast Generator")
    print("=" * 50)
    print("Starting server at http://localhost:5000")
    app.run(debug=True, port=5000)
