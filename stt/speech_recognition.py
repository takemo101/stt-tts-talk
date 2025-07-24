"""音声認識機能を提供するモジュール"""

import speech_recognition as sr  # type: ignore

from .effect import RecEffectPlayer, RecEffectPlayerForMac
from .exceptions import SpeechRecognitionError


class SpeechRecognizer:
    """音声認識を行うクラス"""

    # 周囲音の調整時間と音声認識のタイムアウト時間
    AMBIENT_NOISE_DURATION = 1.0

    # 音声認識のタイムアウト時間
    SPEECH_TIMEOUT = 10.0

    def __init__(
        self, effect_player: RecEffectPlayer = RecEffectPlayerForMac()
    ):
        self._recognizer = sr.Recognizer()
        self._effect_player = effect_player

    def listen(self) -> str:
        """マイクから音声を取得し、テキストに変換する
        Returns:
            str: 認識されたテキスト
        Raises:
            SpeechRecognitionError: 音声認識に失敗した場合
        """
        try:
            with sr.Microphone() as source:
                print('周囲音を調整中...')
                self._recognizer.adjust_for_ambient_noise(
                    source, duration=int(self.AMBIENT_NOISE_DURATION)
                )
                # 音声認識の開始時に効果音を再生
                print('録音中... 話してください')
                self._effect_player.start()
                audio = self._recognizer.listen(
                    source, timeout=self.SPEECH_TIMEOUT
                )

            # 音声認識の終了時に効果音を再生
            print('音声認識中...')
            result: str = self._recognizer.recognize_google(  # type: ignore
                audio, language='ja-JP'
            )

            self._effect_player.end()
            print(f'認識結果: {result}')
            return result

        except sr.UnknownValueError:
            raise SpeechRecognitionError('音声を認識できませんでした')
        except sr.WaitTimeoutError:
            raise SpeechRecognitionError(
                'タイムアウトしました。もう一度話しかけてください。'
            )
        except sr.RequestError as e:
            raise SpeechRecognitionError(
                f'Google Speech Recognition サービスでエラーが発生しました: {e}'
            )
