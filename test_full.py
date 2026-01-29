"""
Complete test: PDF to Podcast with audio generation
"""
import os
import sys
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from app import extract_text_from_pdf, generate_podcast_script, generate_full_podcast

pdf_path = r"D:\new_cast\zeroth review.pdf"
output_path = r"D:\new_cast\outputs\zeroth_review_podcast.mp3"

print("🎙️ PodCast AI - Complete Test")
print("=" * 60)

# Step 1: Extract text
print("\n📄 STEP 1: Extracting text from PDF...")
try:
    text = extract_text_from_pdf(pdf_path)
    print(f"   ✅ Extracted {len(text)} characters")
    print(f"   Preview: {text[:200]}...")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Step 2: Generate script
print("\n🤖 STEP 2: Generating podcast script with AI...")
print("   (This may take 10-30 seconds)")
try:
    script = generate_podcast_script(text)
    print(f"   ✅ Script generated!")
    print(f"   📌 Title: {script.get('title', 'Untitled')}")
    print(f"   📝 Summary: {script.get('summary', 'No summary')}")
    print(f"   💬 Dialogues: {len(script.get('conversation', []))} exchanges")
    
    # Save script
    with open("outputs/script.json", "w", encoding="utf-8") as f:
        json.dump(script, f, indent=2, ensure_ascii=False)
    print("   💾 Script saved to outputs/script.json")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 3: Generate audio
print("\n🎧 STEP 3: Generating podcast audio with male & female voices...")
print("   🔊 Teacher: Male voice (en-US-GuyNeural)")
print("   🔊 Student: Female voice (en-US-JennyNeural)")
print("   (This may take 1-2 minutes depending on script length)")

try:
    output_file = generate_full_podcast(script, output_path)
    
    # Check file size
    file_size = os.path.getsize(output_file)
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"\n   ✅ Podcast generated successfully!")
    print(f"   📁 File: {output_file}")
    print(f"   💾 Size: {file_size_mb:.2f} MB")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("🎉 SUCCESS! Your podcast is ready!")
print(f"🎧 Listen to: {output_path}")
print("🌐 Or use the web app at: http://localhost:5000")
