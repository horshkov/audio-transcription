#!/usr/bin/env python3
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from transcriber import AudioTranscriber

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

transcriber = AudioTranscriber()

SUPPORTED_FORMATS = {
    'mp3', 'mp4', 'm4a', 'wav', 'flac', 'ogg', 'opus',
    'webm', 'aac', 'wma', 'amr', 'avi', 'mov'
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "Send me audio/voice messages or files and I'll transcribe them!\n\n"
        "Supported formats: MP3, MP4, M4A, WAV, FLAC, OGG, and more.\n"
        "Max file size: 20MB (Telegram limit)"
    )

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle audio, voice, video, and document files"""
    try:
        file = None
        file_name = None

        # Determine file type and get file object
        if update.message.audio:
            file = await update.message.audio.get_file()
            file_name = update.message.audio.file_name or "audio.mp3"
        elif update.message.voice:
            file = await update.message.voice.get_file()
            file_name = "voice.ogg"
        elif update.message.video:
            file = await update.message.video.get_file()
            file_name = update.message.video.file_name or "video.mp4"
        elif update.message.video_note:
            file = await update.message.video_note.get_file()
            file_name = "video_note.mp4"
        elif update.message.document:
            file = await update.message.document.get_file()
            file_name = update.message.document.file_name or "file.mp3"

            # Validate format for documents
            ext = file_name.split('.')[-1].lower() if '.' in file_name else ''
            if ext not in SUPPORTED_FORMATS:
                await update.message.reply_text(
                    f"Unsupported format: {ext}\n"
                    f"Supported: {', '.join(sorted(SUPPORTED_FORMATS))}"
                )
                return
        else:
            return

        # Check file size (Telegram limit ~20MB)
        file_size_mb = file.file_size / (1024 * 1024)
        if file_size_mb > 20:
            await update.message.reply_text(
                f"File too large: {file_size_mb:.1f}MB\n"
                "Telegram bot API limit is 20MB"
            )
            return

        await update.message.reply_text(
            f"Processing {file_name} ({file_size_mb:.1f}MB)..."
        )

        # Download file
        file_path = os.path.join("/tmp", file_name)
        await file.download_to_drive(file_path)

        await update.message.reply_text("Transcribing...")

        # Transcribe
        text = transcriber.transcribe(file_path)

        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)

        # Send transcription (split if too long)
        if len(text) > 4000:
            for i in range(0, len(text), 4000):
                await update.message.reply_text(text[i:i+4000])
        else:
            await update.message.reply_text(f"Transcription:\n\n{text}")

    except Exception as e:
        logger.error(f"Error processing media: {e}")
        await update.message.reply_text(f"Error: {str(e)}")

def main():
    """Run the bot"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in .env")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.AUDIO | filters.VOICE | filters.VIDEO |
        filters.VIDEO_NOTE | filters.Document.ALL,
        handle_media
    ))

    logger.info("Bot started. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
