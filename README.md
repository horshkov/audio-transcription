# Audio Transcription Tool

Transcribe audio files using AssemblyAI with multiple interfaces: Telegram bot, CLI, and Python module.

## Features

- **Multiple formats**: MP3, MP4, WAV, M4A, FLAC, OGG, WEBM, and more
- **Telegram bot**: Send audio/voice messages and get instant transcriptions
- **CLI tool**: Command-line interface for batch processing
- **Python module**: Integrate transcription into your applications
- **Large file support**: Up to 20MB via Telegram

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

#### Get AssemblyAI API Key
1. Sign up at [AssemblyAI](https://www.assemblyai.com/)
2. Get your API key from the dashboard
3. Add to `.env`: `ASSEMBLYAI_API_KEY=your_key_here`

#### Get Telegram Bot Token
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow instructions
3. Copy the bot token
4. Add to `.env`: `TELEGRAM_BOT_TOKEN=your_token_here`

## Usage

### Telegram Bot

```bash
python3 telegram_bot.py
```

Send audio or voice messages to the bot and get transcriptions instantly.

### As a module

```python
from transcriber import AudioTranscriber

transcriber = AudioTranscriber()

# Simple transcription
text = transcriber.transcribe("path/to/audio.mp3")
print(text)

# Or use a URL
text = transcriber.transcribe("https://example.com/audio.mp3")

# Detailed transcription
details = transcriber.transcribe_with_details("audio.mp3")
print(details['text'])
```

### CLI

```bash
# Basic transcription
python cli.py path/to/audio.mp3

# With detailed output
python cli.py -d path/to/audio.mp3

# Save to file
python cli.py -o transcript.txt path/to/audio.mp3

# From URL
python cli.py https://assembly.ai/wildfires.mp3
```

## Project Structure

```
audio-transcription/
├── transcriber.py      # Core transcription engine
├── telegram_bot.py     # Telegram bot interface
├── cli.py             # Command-line tool
├── example.py         # Usage examples
├── requirements.txt   # Python dependencies
├── Procfile           # Railway/Heroku deployment
├── railway.json       # Railway configuration
├── .env.example       # Environment template
├── .env              # Your API keys (gitignored)
└── .gitignore        # Protects sensitive files
```

## Deployment

### Production Checklist

- [ ] Copy `.env.example` to `.env` and configure API keys
- [ ] Ensure `.env` is in `.gitignore`
- [ ] Never commit API keys to git
- [ ] Use environment variables in production
- [ ] Monitor API usage and costs

### Deploy to Railway

1. **Connect Repository**
   - Go to [Railway](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `audio-transcription` repository

2. **Configure Environment Variables**
   - Go to project → Variables
   - Add `ASSEMBLYAI_API_KEY` = your_assemblyai_key
   - Add `TELEGRAM_BOT_TOKEN` = your_telegram_token

3. **Deploy**
   - Railway will automatically detect `railway.json` and `Procfile`
   - Bot will start automatically
   - Check logs for "Bot started" message

### Deploy to Render / Heroku

Same process - both platforms use `Procfile`:
- Connect GitHub repository
- Set environment variables in dashboard
- Deploy automatically

### Deploy to Server

```bash
# Clone repository
git clone <your-repo-url>
cd audio-transcription

# Setup environment
cp .env.example .env
# Edit .env with your keys

# Install dependencies
pip install -r requirements.txt

# Run bot
python3 telegram_bot.py
```

### Using systemd (Linux)

Create `/etc/systemd/system/transcription-bot.service`:

```ini
[Unit]
Description=Audio Transcription Telegram Bot
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/audio-transcription
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable transcription-bot
sudo systemctl start transcription-bot
sudo systemctl status transcription-bot
```

## Supported Formats

Audio: MP3, M4A, AAC, FLAC, WAV, WMA, AMR, OGG, OPUS
Video: MP4, AVI, MOV, WEBM (audio track extracted)
