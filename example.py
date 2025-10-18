from transcriber import AudioTranscriber

# Initialize transcriber
transcriber = AudioTranscriber()

# Example 1: Transcribe from URL
print("Transcribing from URL...")
text = transcriber.transcribe("https://assembly.ai/wildfires.mp3")
print(text[:200] + "...\n")

# Example 2: Transcribe with details
print("Getting detailed transcription...")
details = transcriber.transcribe_with_details("https://assembly.ai/wildfires.mp3")
print(f"ID: {details['id']}")
print(f"Status: {details['status']}")
print(f"Duration: {details['audio_duration']}s")
print(f"Text preview: {details['text'][:100]}...")

# Example 3: Transcribe local file
# text = transcriber.transcribe("./my_audio.mp3")
# print(text)
