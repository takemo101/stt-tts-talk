"""STT (Speech-to-Text) および TTS (Text-to-Speech) 機能を提供するパッケージ"""

from .ai_chat import AIChat
from .config import (
    CHARACTER_MAP,
    GEMINI_MODEL,
    SYSTEM_INSTRUCTION_TEMPLATE,
    TALK_END_KEYWORD,
    CharacterID,
    CharacterOptions,
)
from .exceptions import (
    AIResponseError,
    EnvironmentError,
    SpeechRecognitionError,
    STTAppError,
    VoiceSynthesisError,
)
from .googlevoice import GoogleTTSClient
from .nijivoice import NijiVoiceClient
from .speech_recognition import SpeechRecognizer
from .talk import TalkController
from .voice import VoiceClient, is_installed, play

__all__ = [
    # AI チャット
    'AIChat',
    # 設定とキャラクター
    'CHARACTER_MAP',
    'GEMINI_MODEL',
    'SYSTEM_INSTRUCTION_TEMPLATE',
    'TALK_END_KEYWORD',
    'CharacterID',
    'CharacterOptions',
    # 例外クラス
    'AIResponseError',
    'EnvironmentError',
    'SpeechRecognitionError',
    'STTAppError',
    'VoiceSynthesisError',
    # 音声合成クライアント
    'GoogleTTSClient',
    'NijiVoiceClient',
    'VoiceClient',
    # 音声認識
    'SpeechRecognizer',
    # 会話制御
    'TalkController',
    # ユーティリティ関数
    'is_installed',
    'play',
]
