import io
import wave

from google.genai import Client, types  # type: ignore

from .config import CharacterID
from .voice import VoiceClient


class GoogleTTSClient(VoiceClient):
    """Google TTS API のクライアント
    このクライアントを使用してにじGoogle TTS APIでテキストを音声に変換できます。
    Attributes:
        _client (Client): Google GenAI クライアント
        _voice_name (str): 音声の名前
    """

    # キャラクターIDと音声IDのマッピング
    CHARACTER_VOICE_MAP: dict[CharacterID, str] = {
        'gyaru': 'Kore',
        'shy': 'Leda',
        'ikemen': 'Zephyr',
    }

    def __init__(self, client: Client, voice_name: str):
        self._client = client
        self._voice_name = voice_name

    async def text_to_speech(self, text: str) -> bytes:
        """Google TTS API を使用してテキストを音声に変換する
        Args:
            text (str): 音声に変換するテキスト
        Returns:
            bytes: バイト形式の音声データ
        Raises:
            ValueError: API レスポンスに base64 音声データが含まれていない場合
        """

        response = self._client.models.generate_content(
            model='gemini-2.5-flash-preview-tts',
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=['AUDIO'],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=self._voice_name,
                        ),
                    )
                ),
            ),
        )

        candidates = response.candidates

        # ガード句: 応答が存在し、音声データが含まれているか確認
        if (
            candidates
            and candidates[0].content
            and candidates[0].content.parts
            and candidates[0].content.parts[0].inline_data
        ):
            data = candidates[0].content.parts[0].inline_data.data
        else:
            raise ValueError('APIから音声データが受信されませんでした。')

        if not data:
            raise ValueError('APIから音声データが受信されませんでした。')

        return self._convert_to_wav(data)

    def _convert_to_wav(self, audio: bytes) -> bytes:
        """音声データを WAV 形式に変換する
        Args:
            audio_data (bytes): 音声データ
        Returns:
            bytes: WAV 形式の音声データ
        """

        # 音声データをバイト形式に変換
        buffer = io.BytesIO(audio)

        # wave モジュールを使用してバイトデータを WAV 形式に変換
        with wave.open(buffer, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            wf.writeframes(audio)

        return buffer.getvalue()

    @classmethod
    def create_from_character_id(
        cls, client: Client, character_id: CharacterID
    ) -> 'GoogleTTSClient':
        """キャラクターIDから GoogleTTSClient を作成する

        Args:
            client (Client): Google GenAI クライアント
            id (CharacterID): キャラクターの識別子

        Returns:
            GoogleTTSClient: Google TTS クライアントインスタンス
        """

        voice_name = cls.CHARACTER_VOICE_MAP.get(character_id)

        if voice_name is None:
            raise ValueError(f'Unknown character ID: {character_id}')

        return cls(client=client, voice_name=voice_name)
