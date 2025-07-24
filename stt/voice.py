import io
import shutil
import subprocess
from abc import ABC, abstractmethod


class VoiceClient(ABC):
    """API のクライアント
    このクライアントを使用してテキストを音声に変換できます。
    """

    @abstractmethod
    async def text_to_speech(self, text: str) -> bytes:
        """API を使用してテキストを音声に変換する
        Args:
            text (str): 音声に変換するテキスト
        Returns:
            bytes: バイト形式の音声データ
        Raises:
            ValueError: API レスポンスに base64 音声データが含まれていない場合
        """
        pass


def is_installed(lib_name: str) -> bool:
    """指定されたライブラリがインストールされているか確認する
    Args:
        lib_name (str): 確認するライブラリの名前
    Returns:
        bool: ライブラリがインストールされている場合は True、そうでない場合は False
    """
    lib = shutil.which(lib_name)
    if lib is None:
        return False
    return True


def play(
    audio: bytes,
    use_ffmpeg: bool = True,
) -> None:
    """ffplay または sounddevice を使用して音声を再生する
    Args:
        audio (bytes): バイト形式の音声データ
        use_ffmpeg (bool): 再生に ffplay を使用するかどうか。デフォルトは True
    Raises:
        ValueError: use_ffmpeg が True で ffplay がインストールされていない場合
        ValueError: use_ffmpeg が False で sounddevice または soundfile がインストールされていない場合
    """

    if use_ffmpeg:
        # ffplay を使用して音声を再生する
        if not is_installed('ffplay'):
            raise ValueError(
                '`ffplay` がインストールされていません。音声再生を使用するにはインストールしてください。'
            )

        args = ['ffplay', '-autoexit', '-', '-nodisp']
        proc = subprocess.Popen(
            args=args,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        _out, _err = proc.communicate(input=audio)
        proc.poll()
    else:
        # sounddevice と soundfile を使用して音声を再生する
        try:
            import sounddevice as sd  # type: ignore
            import soundfile as sf  # type: ignore
        except ModuleNotFoundError:
            message = '`use_ffmpeg=False` の場合は `uv add sounddevice soundfile` が必要です'
            raise ValueError(message)

        data, samplerate = sf.read(io.BytesIO(audio))

        sd.play(data, samplerate)
        sd.wait()
