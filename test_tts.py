"""
Test Edge TTS with male and female voices
"""
import asyncio
import edge_tts

# Voices
MALE_VOICE = "en-US-GuyNeural"      # Deep male voice (Teacher)
FEMALE_VOICE = "en-US-JennyNeural"  # Natural female voice (Student)

async def test_tts():
    print("🎙️ Testing Edge TTS - Male & Female Voices")
    print("=" * 50)
    
    # Test 1: Male voice (Teacher)
    print("\n📢 Test 1: Male voice (Teacher - Guy)")
    try:
        teacher_text = "Hello everyone! Today we're going to explore how artificial intelligence is revolutionizing train traffic management. This is a fascinating topic that combines computer science with real-world infrastructure."
        communicate = edge_tts.Communicate(teacher_text, MALE_VOICE)
        await communicate.save("test_teacher.mp3")
        print("   ✅ Success! Saved test_teacher.mp3")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Female voice (Student)
    print("\n📢 Test 2: Female voice (Student - Jenny)")
    try:
        student_text = "That sounds really interesting! Can you explain how the AI actually makes decisions about which trains should go first? I'm curious about the algorithm behind it."
        communicate = edge_tts.Communicate(student_text, FEMALE_VOICE)
        await communicate.save("test_student.mp3")
        print("   ✅ Success! Saved test_student.mp3")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Test complete!")
    print("🎧 Listen to: test_teacher.mp3 (male) and test_student.mp3 (female)")

# Run the async test
asyncio.run(test_tts())
