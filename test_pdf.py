"""
Quick test script to process the PDF and generate podcast
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from app import extract_text_from_pdf, generate_podcast_script, GROQ_API_KEY

pdf_path = r"D:\new_cast\zeroth review.pdf"

print("🎙️ PodCast AI - Quick Test")
print("=" * 50)
print(f"API Key: {GROQ_API_KEY[:20]}..." if GROQ_API_KEY else "No API Key!")
print()

# Step 1: Extract text
print("📄 Step 1: Extracting text from PDF...")
try:
    text = extract_text_from_pdf(pdf_path)
    print(f"   ✅ Extracted {len(text)} characters")
    print(f"   Preview: {text[:300]}...")
    print()
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Step 2: Generate script
print("🤖 Step 2: Generating podcast script with AI...")
print("   (This may take 10-30 seconds)")
try:
    script = generate_podcast_script(text)
    print(f"   ✅ Script generated!")
    print(f"   Title: {script.get('title', 'Untitled')}")
    print(f"   Summary: {script.get('summary', 'No summary')}")
    print(f"   Dialogues: {len(script.get('conversation', []))} exchanges")
    print()
    
    # Print conversation
    print("📝 Conversation Preview:")
    print("-" * 40)
    for i, dialogue in enumerate(script.get('conversation', [])[:4]):
        speaker = dialogue.get('speaker', 'Unknown')
        text = dialogue.get('text', '')
        icon = '👨‍🏫' if speaker == 'teacher' else '👨‍🎓'
        print(f"{icon} {speaker.upper()}: {text[:100]}...")
        print()
    
    if len(script.get('conversation', [])) > 4:
        print(f"   ... and {len(script['conversation']) - 4} more dialogues")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 50)
print("✅ Test completed successfully!")
print("🌐 Open http://localhost:5000 in your browser to use the full app!")
