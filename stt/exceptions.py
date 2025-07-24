"""アプリケーション固有の例外クラス"""


class STTAppError(Exception):
    """STTアプリケーションのベース例外クラス"""

    pass


class EnvironmentError(STTAppError):
    """環境変数関連のエラー"""

    pass


class SpeechRecognitionError(STTAppError):
    """音声認識関連のエラー"""

    pass


class AIResponseError(STTAppError):
    """AI応答関連のエラー"""

    pass


class VoiceSynthesisError(STTAppError):
    """音声合成関連のエラー"""

    pass
