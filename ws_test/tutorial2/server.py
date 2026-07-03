import asyncio
import websockets


connected_clients = set()
shutdown_event = asyncio.Event()

async def dist_handler(websocket):
    connected_clients.add(websocket)
    print(f"\n[接続] 新規クライアント（現在の接続数: {len(connected_clients)}）")
    print("サーバーコマンド用プロンプト: ", end="", flush=True)
    
    try:
        async for message in websocket:
            # 受信したメッセージを他の全員に転送
            broadcast_tasks = [
                client.send(message) for client in connected_clients if client != websocket
            ]
            if broadcast_tasks:
                await asyncio.gather(*broadcast_tasks)
    except websockets.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)
        print(f"\n[切断] クライアントが離脱しました（現在の接続数: {len(connected_clients)}）")
        print("サーバーコマンド用プロンプト: ", end="", flush=True)

# 【追加】サーバーのターミナル入力を監視するタスク
async def watch_server_input():
    try:
        while True:
            # サーバー側のターミナルでの入力を非同期で待つ
            server_input = await asyncio.to_thread(input, "サーバーコマンド用プロンプト: ")
            if server_input.strip() == "exit":
                print("終了処理を開始します...")
                shutdown_event.set()  # サーバー停止フラグを立てる
                break
    except Exception as e:
        print(f"エラーが発生しました: {e}")

async def main():
    async with websockets.serve(dist_handler, "localhost", 8765):
        print("双方向チャットサーバーが起動しました（port: 8765）...")
        print("※サーバーを終了するには、この画面で 'exit' と入力してEnterを押してください。")
        
        # ターミナル監視タスクを並行して走らせる
        input_task = asyncio.create_task(watch_server_input())
        
        # 終了フラグが立つまで待機
        await shutdown_event.wait()
        
        # タスクの後片付け
        input_task.cancel()
        
    print("サーバーが安全にシャットダウンされました。")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCtrl+Cにより強制終了されました。")