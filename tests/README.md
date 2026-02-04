# Tests

## Running Tests

### Quick Manual Test
```bash
# Set environment variables in .env file
python tests/manual_test.py
```

### Unit Tests (no credentials needed)
```bash
pip install pytest pytest-mock
pytest tests/ --ignore=tests/integration/ -v
```

### Integration Tests (requires credentials)
```bash
pytest tests/integration/ -v
```

## Required Environment Variables

- `APP_ID` - Agora App ID
- `APP_CERTIFICATE` - Agora App Certificate  
- `API_KEY` - Agora Customer ID
- `API_SECRET` - Agora Customer Secret
- `LLM_API_KEY` - OpenAI API Key
- `ASR_DEEPGRAM_API_KEY` - Deepgram API Key (optional)
- `TTS_ELEVENLABS_API_KEY` - ElevenLabs API Key (optional)
