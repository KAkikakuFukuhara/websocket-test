# README

一つのサーバーと複数のクライアントでの通信。  
あるクライアントから送られたメッセージをサーバーが受取、複数のクライアントに配布する。  
実験の目的としては以下の２つを実行する。  
* クライアント→サーバー通信
* サーバー→クライアント通信

## 実行方法  

* サーバー起動
```
python ws_test/tutorial2/server.py
```

* クライアント起動  

クライアント起動では複数のクライアントを同一プログラムで実行するので２つ以上のターミナルを開いて以下のプログラムをそれぞれで実行する。  
```
# terminal1
python ws_test/tutorial2/client.py
```
```
# terminal2
python ws_test/tutorial2/client.py
```




