import asyncio
import websockets
import sys

# サーバーからのメッセージを常に監視して表示するタスク
async def receive_messages(websocket):
    try:
        async for message in websocket:
            # 自分が文字入力中であっても、受信したら割り込んで画面に表示される
            print(f"\n[受信] {message}")
            print("> ", end="", flush=True) # 入力プロンプトを再表示
    except websockets.ConnectionClosed:
        print("\nサーバーとの接続が切れました。")

# ユーザーの入力を常に監視して送信するタスク
async def send_messages(websocket):
    try:
        while True:
            # キーボード入力を非同期で待つ
            user_input = await asyncio.to_thread(input, "> ")
            if user_input.strip() == "exit":
                break
            if user_input:
                await websocket.send(user_input)
    except Exception as e:
        print(f"エラーが発生しました: {e}")

async def main():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print("サーバーに接続しました。'exit'で終了。")
        
        # タスクをそれぞれオブジェクトとして作成
        receive_task = asyncio.create_task(receive_messages(websocket))
        send_task = asyncio.create_task(send_messages(websocket))
        
        # まず「送信タスク」が終わるのを待つ（exitが入力されるまで）
        await send_task
        
        # 送信タスクが終わったら、受信タスクを強制終了（キャンセル）する
        receive_task.cancel()
        
        # 受信タスクが完全に終了するのを一瞬待つ
        await asyncio.gather(receive_task, return_exceptions=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n強制終了されました。")