# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.3] - 2025-02-04

### Added
- ✨ **Complete vendor support** - Added configuration classes for all built-in ASR/TTS vendors
  - ASR: `FengmingASRConfig`, `TencentASRConfig`, `MicrosoftASRConfig`, `AresASRConfig`
  - TTS: `MinimaxTTSConfig`, `TencentTTSConfig`, `BytedanceTTSConfig`, `MicrosoftTTSConfig`, `CartesiaTTSConfig`, `OpenAITTSConfig`
- ✨ **Custom vendor support** - Users can now use any ASR/TTS provider by providing custom `params`
- Added comprehensive documentation for all supported vendors

### Changed
- **User-friendly API** - Configuration classes now use dataclass wrappers with sensible defaults
  - Only required field is `api_key` for most vendors
  - All other fields have sensible defaults
  - Example: `DeepgramASRConfig(api_key="xxx")` - that's it!
  - Internally uses Pydantic models from `join.py` for validation (via `to_pydantic()` method)
- Enhanced `PropertyBuilder` to support all built-in vendors from Agora REST API
- Improved error messages to guide users on vendor usage
- Updated README with complete vendor list and simplified usage examples

### Coverage
- ASR: 5/5 vendors (100% coverage)
- TTS: 7/7 vendors (100% coverage)
- LLM: Full support for OpenAI-compatible APIs

### Examples
```python
# Simple usage - only api_key required
asr = DeepgramASRConfig(api_key="xxx")
tts = ElevenLabsTTSConfig(api_key="xxx")

# Optional: customize with defaults
asr.language = "zh-CN"
tts.voice_id = "custom_voice"

# Dict usage (backward compatible)
asr = {"vendor": "deepgram", "api_key": "xxx"}

# Custom vendor (advanced)
asr = {"vendor": "custom", "params": {"api_key": "xxx", "custom_param": "value"}}
```

## [0.1.2] - 2025-02-04

### Changed
- **BREAKING**: Removed `AgentClient.generate_config()` method - users now manually generate channel, UIDs, and token for more transparency
- **BREAKING**: Removed `AgentClient.generate_agent_token()` method - users should use `TokenBuilder.generate()` directly
- Renamed configuration classes for clarity:
  - `ASRConfig` → `DeepgramASRConfig` (old name kept as alias for backward compatibility)
  - `LLMConfig` → `OpenAILLMConfig` (old name kept as alias for backward compatibility)
  - `TTSConfig` → `ElevenLabsTTSConfig` (old name kept as alias for backward compatibility)
- Updated UID generation to use `random.randint(100000, 999999)` for valid 6-digit UIDs
- Improved API transparency - users have full control over connection configuration

### Added
- Base configuration classes (`BaseASRConfig`, `BaseLLMConfig`, `BaseTTSConfig`) for custom implementations
- `TokenBuilder` now exported from `agora_rest.agent` submodule
- Better examples showing explicit configuration generation

### Fixed
- Fixed "agent_rtc_uid invalid" error by using proper UID format
- Fixed test suite to work with new API structure

## [0.1.1] - 2025-01-29

### Changed
- Reorganized public API exports - Agent-related classes now exported from `agora_rest.agent` submodule
- Simplified API by removing `AgentConfig` class
- `AgentClient` constructor now accepts explicit parameters instead of config object
- Removed unused `PORT` environment variable

### Added
- Direct parameter passing to `AgentClient` constructor
- More flexible configuration approach

## [0.1.0] - 2025-01-28

### Added
- Initial release of Agora REST Client Python SDK
- High-level Agent API for managing Conversational AI Agents
- AgentClient for core business logic and API calls
- Support for Deepgram ASR
- Support for OpenAI LLM
- Support for ElevenLabs TTS
- TokenBuilder for generating Agora tokens
- PropertyBuilder for building agent properties
- Configuration components (ASRConfig, LLMConfig, TTSConfig)
- Comprehensive documentation and examples

### Features
- Environment variable based configuration
- Type-safe API with full type hints
- Automatic token generation
- Three-tier configuration (ASR, LLM, TTS)
- Error handling and validation
- Retry mechanism for API calls

[Unreleased]: https://github.com/AgoraIO-Community/agora-rest-client-python/compare/v0.1.3...HEAD
[0.1.3]: https://github.com/AgoraIO-Community/agora-rest-client-python/releases/tag/v0.1.3
[0.1.2]: https://github.com/AgoraIO-Community/agora-rest-client-python/releases/tag/v0.1.2
[0.1.1]: https://github.com/AgoraIO-Community/agora-rest-client-python/releases/tag/v0.1.1
[0.1.0]: https://github.com/AgoraIO-Community/agora-rest-client-python/releases/tag/v0.1.0
