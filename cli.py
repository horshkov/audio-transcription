#!/usr/bin/env python3
import sys
import argparse
from transcriber import AudioTranscriber

def main():
    parser = argparse.ArgumentParser(description="Transcribe audio files using AssemblyAI")
    parser.add_argument("audio_source", help="Path to audio file or URL")
    parser.add_argument("-d", "--detailed", action="store_true", help="Show detailed output")
    parser.add_argument("-o", "--output", help="Save transcription to file")

    args = parser.parse_args()

    try:
        transcriber = AudioTranscriber()

        if args.detailed:
            result = transcriber.transcribe_with_details(args.audio_source)
            print(f"Transcription ID: {result['id']}")
            print(f"Status: {result['status']}")
            print(f"Duration: {result['audio_duration']}s")
            print(f"\nTranscript:\n{result['text']}")
            text = result['text']
        else:
            text = transcriber.transcribe(args.audio_source)
            print(text)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(text)
            print(f"\nSaved to {args.output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
