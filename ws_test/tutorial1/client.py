import asyncio
import websockets

async def send_message():
    uri = "ws://localhost:8765"
    
    # サーバーに接続
    async with websockets.connect(uri) as websocket:
        message = "こんにちは、サーバーさん！"
        print(f"送信: {message}")
        await websocket.send(message)

        # サーバーからの返答を受信
        response = await websocket.recv()
        print(f"受信: {response}")

if __name__ == "__main__":
    asyncio.run(send_message())