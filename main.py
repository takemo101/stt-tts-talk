"""音声対話アプリケーションのメインモジュール"""

import asyncio
import os
import random
from typing import Literal

from dotenv import load_dotenv

from stt.ai_chat import AIChat
from stt.config import (
    CHARACTER_MAP,
    GEMINI_MODEL,
    SYSTEM_INSTRUCTION_TEMPLATE,
    TALK_END_KEYWORD,
    CharacterOptions,
)
from stt.googlevoice import GoogleTTSClient
from stt.nijivoice import NijiVoiceClient
from stt.talk import TalkController

load_dotenv()  # 環境変数の読み込み


async def talk(
    mode: Literal['nijivoice', 'google'] = 'nijivoice',
    character: CharacterOptions = random.choice(CHARACTER_MAP),
) -> None:
    """音声対話を開始するメイン関数
    Args:
        mode (Literal['nijivoice', 'google']): 使用する音声合成サービスのモード
        character (CharacterOptions): 対話に使用するキャラクターのオプション
    Raises:
        OSError: 必要な環境変数が設定されていない場合
    """

    # Gemini APIキーを取得
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        raise OSError('GEMINI_API_KEYが設定されていません。')

    # にじボイス APIキーを取得
    nijivoice_api_key = os.getenv('NIJIVOICE_API_KEY')
    if not nijivoice_api_key:
        raise OSError('NIJIVOICE_API_KEYが設定されていません。')

    print(f'選択されたキャラクター: {character.name}')

    ai_chat = AIChat(
        system_instruction=SYSTEM_INSTRUCTION_TEMPLATE.format(
            character_name=character.name,
            character_instruction=character.instruction,
        ),
        model=GEMINI_MODEL,
        api_key=gemini_api_key,
    )

    # 会話コントローラーを作成して会話を開始
    controller = TalkController(
        character_name=character.name,
        talk_end_keyword=TALK_END_KEYWORD,
        ai_chat=ai_chat,
        # 音声クライアントの選択
        # `nijivoice` モードでは NijiVoiceClient を使用
        # `google` モードでは GoogleTTSClient を使用
        voice_client=NijiVoiceClient.create_from_character_id(
            api_key=nijivoice_api_key,
            character_id=character.id,
        )
        if mode == 'nijivoice'
        else GoogleTTSClient.create_from_character_id(
            client=ai_chat.client,
            character_id=character.id,
        ),
    )

    await controller.start_talk()


def main():
    asyncio.run(talk())


if __name__ == '__main__':
    main()
