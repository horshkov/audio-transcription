# Security Guidelines

## Credentials Protection

### What's Protected

✅ `.env` - Contains actual API keys (gitignored)
✅ All credentials loaded from environment variables only
✅ No hardcoded secrets in codebase

### Before Deploying

#### Pre-commit Checklist

```bash
# 1. Verify .env is gitignored
git status

# Should NOT see .env in the list
# Should see .env.example

# 2. Check for accidental credential leaks
grep -r "d34589f76c2c43a6b44ad01db6c6ef51" . --exclude-dir=.git --exclude=.env
grep -r "8200330986:AAF" . --exclude-dir=.git --exclude=.env

# Should return no results (or only .env)

# 3. Verify .env.example has placeholders only
cat .env.example

# Should show placeholder text, not actual keys
```

#### Production Deployment

1. **Never commit `.env`** - Always use `.env.example` as template
2. **Use server environment variables** - Set in hosting platform
3. **Rotate keys if exposed** - Get new keys from providers
4. **Monitor usage** - Check API dashboards for unusual activity

### Environment Variables

All sensitive data is in these variables:

- `ASSEMBLYAI_API_KEY` - AssemblyAI transcription service
- `TELEGRAM_BOT_TOKEN` - Telegram bot authentication

### If Credentials are Leaked

1. **Immediately revoke** exposed keys
2. **Generate new keys** from service providers
3. **Update `.env`** with new keys
4. **Review git history** - Use `git filter-branch` if needed
5. **Monitor accounts** for unauthorized usage

## File Permissions

Recommended permissions for production:

```bash
chmod 600 .env          # Only owner can read/write
chmod 644 .env.example  # Everyone can read template
chmod 755 *.py          # Scripts executable by all
```

## Hosting Platforms

### Railway / Render / Heroku

Set environment variables in platform dashboard:
- Navigate to Settings → Environment Variables
- Add `ASSEMBLYAI_API_KEY` and `TELEGRAM_BOT_TOKEN`
- Deploy without `.env` file

### Docker

Use docker secrets or env files:

```dockerfile
# .env file should not be in image
# Pass at runtime:
docker run --env-file .env transcription-bot
```

### VPS / Dedicated Server

```bash
# Use systemd environment files
sudo nano /etc/systemd/system/transcription-bot.service

[Service]
EnvironmentFile=/path/to/.env
ExecStart=/usr/bin/python3 telegram_bot.py
```

## Audit Trail

- Last security review: 2025-10-18
- No known credential leaks
- All secrets properly gitignored
