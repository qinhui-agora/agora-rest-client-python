# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/AgoraIO-Community/agora-rest-client-python/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/AgoraIO-Community/agora-rest-client-python/releases/tag/v0.1.2
[0.1.1]: https://github.com/AgoraIO-Community/agora-rest-client-python/releases/tag/v0.1.1
[0.1.0]: https://github.com/AgoraIO-Community/agora-rest-client-python/releases/tag/v0.1.0
