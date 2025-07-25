from abc import ABC, abstractmethod


class OutputWriter(ABC):
    """出力制御を行うインターフェース"""

    @abstractmethod
    def print(self, message: str) -> None:
        """メッセージを出力する

        Args:
            message: 出力するメッセージ
        """
        pass


class StandardOutputWriter(OutputWriter):
    """標準出力を使用する出力制御クラス"""

    def print(self, message: str) -> None:
        """標準出力にメッセージを出力する"""
        print(message)


class SilentOutputWriter(OutputWriter):
    """無音の出力制御クラス（何も出力しない）"""

    def print(self, message: str) -> None:
        """何も出力しない"""
        pass
