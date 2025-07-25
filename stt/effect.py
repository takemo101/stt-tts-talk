import os
from abc import ABC, abstractmethod


class EffectPlayer(ABC):
    """録音効果音の抽象クラス"""

    @abstractmethod
    def start(self) -> None:
        """録音開始時の効果音を再生する"""
        pass

    @abstractmethod
    def end(self) -> None:
        """録音終了時の効果音を再生する"""
        pass


class EffectPlayerForMac(EffectPlayer):
    """macOS用の録音効果音クラス"""

    def start(self) -> None:
        os.system('afplay /System/Library/Sounds/Tink.aiff')

    def end(self) -> None:
        os.system('afplay /System/Library/Sounds/Purr.aiff')
