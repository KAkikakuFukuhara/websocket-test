import asyncio
import websockets

async def echo_handler(websocket):
    print("クライアントが接続しました")
    try:
        # 接続が維持されている間、メッセージを待ち受ける
        async for message in websocket:
            print(f"受信メッセージ: {message}")

            response = f"サーバーからの返信: {type(message)}"
            await websocket.send(response)
    except websockets.ConnectionClosed:
        print("クライアントが切断しました")

async def main():
    # localhostのポート8765でサーバーを起動
    async with websockets.serve(echo_handler, "localhost", 8765):
        print("WebSocketサーバーが起動しました（port: 8765）...")
        await asyncio.Future()  # サーバーを永続的に実行

if __name__ == "__main__":
    asyncio.run(main())