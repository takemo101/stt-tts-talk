from google.genai import Client, chats, types  # type: ignore

from .exceptions import AIResponseError


class AIChat:
    """AI チャット機能を提供するクラス
    Attributes:
        _system_instruction (str): システムインストラクション
        _model (str): 使用するモデル名
        _client (Client): Google GenAI クライアント
    """

    _chat: chats.Chat | None = None

    def __init__(self, system_instruction: str, model: str, client: Client):
        self._system_instruction = system_instruction
        self._model = model
        self._client = client

    def _create_chat(self) -> chats.Chat:
        """チャットセッションを作成する"""
        return self._client.chats.create(
            model=self._model,
            config=types.GenerateContentConfig(
                system_instruction=self._system_instruction,
            ),
        )

    def send_message(self, message: str) -> str:
        """メッセージを送信し、応答を取得する
        Args:
            message: 送信するメッセージ
        Returns:
            str: AI の応答テキスト
        Raises:
            AIResponseError: AI の応答が空の場合
        """

        # チャットセッションが未作成の場合は新規作成
        if self._chat is None:
            self._chat = self._create_chat()

        response: types.GenerateContentResponse = self._chat.send_message(
            message=message
        )

        response_text = response.text
        if not response_text:
            raise AIResponseError('AIの返答がありません。')

        return response_text
