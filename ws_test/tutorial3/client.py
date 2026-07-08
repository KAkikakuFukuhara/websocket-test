
"""
概要: プログラムの概要をここに書く
"""
from typing import List, Dict, Type
from argparse import ArgumentParser
from abc import ABC, abstractmethod
import asyncio
import json

import websockets


def add_arguments(parser: ArgumentParser) -> ArgumentParser:
    # 引数をここに記述
    parser.add_argument('--type', type=str, choices=["str", "json", "bytes"], default='str', help='')
    return parser


def main(*args, **kwargs):
    # 処理をここに記述
    print("Hello, World!")
    asyncio.run(send_message(kwargs['type']))


async def send_message(msg_type:str):
    uri = "ws://localhost:8765"

    type2sender: Dict[str, Type[WebsocketSenderBase]] = {
        'str': StrSender,
        'json': JsonSender,
        'bytes': BytesSender,
    }

    # サーバーに接続
    async with websockets.connect(uri) as websocket:
        sender: ISend = type2sender[msg_type](websocket)
        message = "こんにちは、サーバーさん！"
        print(f"送信: {message}")
        await sender.send(message)

        # サーバーからの返答を受信
        response = await websocket.recv()
        print(f"受信: {response}")



class ISend(ABC):
    @abstractmethod
    async def send(self, msg: str):
        pass



class WebsocketSenderBase(ISend):
    def __init__(self, ws:websockets.ClientConnection):
        self.ws: websockets.ClientConnection = ws



class StrSender(WebsocketSenderBase):
    async def send(self, msg: str):
        print(msg)
        await self.ws.send(msg)



class JsonSender(WebsocketSenderBase):
    async def send(self, msg: str):

        json_text = json.dumps(
            {'msg':msg}
        )
        await self.ws.send(json_text)



class BytesSender(WebsocketSenderBase):
    async def send(self, msg: str):
        msg_bytes = msg.encode()
        await self.ws.send(msg_bytes)



if __name__ == '__main__':
    parser: ArgumentParser = ArgumentParser()
    psrser = add_arguments(parser)
    main(**vars(parser.parse_args()))
