from .ai_chat import AIChat
from .exceptions import VoiceSynthesisError
from .output import OutputWriter, StandardOutputWriter
from .speech_recognition import SpeechRecognizer
from .voice import VoiceClient, play


class TalkController:
    """音声会話を制御するメインクラス
    Attributes:
        _character_name (str): キャラクターの名前
        _talk_end_keyword (str): 会話終了キーワード
        _ai_chat (AIChat): AI チャットインスタンス
        _voice_client (VoiceClient): 音声合成クライアント
        _output (OutputWriter): 出力制御を行うインターフェース
    """

    def __init__(
        self,
        character_name: str,
        talk_end_keyword: str,
        ai_chat: AIChat,
        voice_client: VoiceClient,
        output_writer: OutputWriter = StandardOutputWriter(),
    ):
        self._character_name = character_name
        self._talk_end_keyword = talk_end_keyword
        self._output = output_writer
        self._speech_recognizer = SpeechRecognizer(output_writer=output_writer)

        self._ai_chat = ai_chat
        self._voice_client = voice_client

    async def start_talk(self) -> None:
        """会話を開始する"""
        self._output.print('何か話しかけてください...')

        while True:
            try:
                # 音声認識
                user_input = self._speech_recognizer.listen()

                # 会話終了チェック
                if self._talk_end_keyword in user_input:
                    self._output.print('音声認識を終了します。')
                    break

                # AI 応答生成
                ai_response = self._ai_chat.send_message(user_input)
                self._output.print(
                    f'{self._character_name}の返答: {ai_response}'
                )

                # 音声再生
                await self._play(ai_response)

            except Exception as e:
                self._output.print(f'エラーが発生しました: {e}')
                continue

    async def _play(self, text: str) -> None:
        """テキストを音声合成して再生する"""
        try:
            audio = await self._voice_client.text_to_speech(text)
            play(audio)
        except Exception as e:
            raise VoiceSynthesisError(
                f'音声合成でエラーが発生しました: {e}'
            ) from e
