import base64

import httpx

from .config import CharacterID
from .voice import VoiceClient


class NijiVoiceClient(VoiceClient):
    """にじボイス API のクライアント
    このクライアントを使用してにじボイス APIでテキストを音声に変換できます。
    Attributes:
        _api_key (str): にじボイス の API キー
        _voice_id (str): テキスト読み上げに使用する音声ID
    """

    # APIのベースURL
    BASE_URL = 'https://api.nijivoice.com/api/platform/v1'

    # キャラクターIDと音声IDのマッピング
    CHARACTER_VOICE_MAP: dict[CharacterID, str] = {
        'gyaru': '8c08fd5b-b3eb-4294-b102-a1da00f09c72',
        'shy': '2f982b65-dbc3-4ed6-b355-b0f7c0abaa70',
        'ikemen': '04c7f4e0-41d8-4d02-9cbe-bf79e635f5ab',
    }

    def __init__(self, api_key: str, voice_id: str):
        self._api_key = api_key
        self._voice_id = voice_id

    async def text_to_speech(self, text: str) -> bytes:
        """にじボイス API を使用してテキストを音声に変換する
        Args:
            text (str): 音声に変換するテキスト
        Returns:
            bytes: バイト形式の音声データ
        Raises:
            ValueError: API レスポンスに base64 音声データが含まれていない場合
        """

        headers = {
            'x-api-key': self._api_key,
            'Content-Type': 'application/json',
        }
        data = {'script': text, 'speed': '1.0', 'format': 'wav'}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f'{self.BASE_URL}/voice-actors/{self._voice_id}/generate-encoded-voice',
                headers=headers,
                json=data,
            )
            response.raise_for_status()

        data = response.json()

        base64_audio: str | None = data['generatedVoice']['base64Audio']

        if base64_audio is None:
            raise ValueError('レスポンスに Base64 音声データがありません。')

        return base64.b64decode(base64_audio)

    @classmethod
    def create_from_character_id(
        cls, api_key: str, character_id: CharacterID
    ) -> 'NijiVoiceClient':
        """キャラクターIDから NijiVoiceClient を作成する

        Args:
            api_key (str): にじボイス API キー
            id (CharacterID): キャラクターの識別子

        Returns:
            NijiVoiceClient: にじボイスクライアントインスタンス
        """

        voice_id = cls.CHARACTER_VOICE_MAP.get(character_id)

        if voice_id is None:
            raise ValueError(f'Unknown character ID: {character_id}')

        return cls(api_key=api_key, voice_id=voice_id)
