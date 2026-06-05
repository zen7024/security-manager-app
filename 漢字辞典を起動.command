#!/bin/bash
# ============================================================
# 漢字辞典 ランチャー
# ダブルクリックで起動 → Googleの本物の手書き認識が使えます
# ============================================================

# スクリプトと同じフォルダに移動
cd "$(dirname "$0")"

PORT=8765
HTML_FILE="漢字辞典.html"

# HTMLファイルの存在確認
if [ ! -f "$HTML_FILE" ]; then
  osascript -e 'display dialog "エラー：漢字辞典.html が見つかりません。\n同じフォルダに置いてください。" buttons {"OK"} default button "OK"'
  exit 1
fi

# すでに同じポートでサーバーが動いていたら止める
if lsof -i :"$PORT" > /dev/null 2>&1; then
  lsof -ti :"$PORT" | xargs kill -9 2>/dev/null
  sleep 0.3
fi

# Python3でHTTPサーバーを起動（バックグラウンド）
python3 -m http.server $PORT --bind 127.0.0.1 > /tmp/kanji_server.log 2>&1 &
SERVER_PID=$!

sleep 0.8

# ブラウザで開く
open "http://localhost:$PORT/$HTML_FILE"

echo "======================================"
echo " 漢字辞典サーバー起動中"
echo " URL: http://localhost:$PORT/$HTML_FILE"
echo " PID: $SERVER_PID"
echo "======================================"
echo " ブラウザを閉じてもサーバーは動き続けます"
echo " 終了するにはこのウィンドウを閉じてください"
echo "======================================"

# Ctrl+C または ウィンドウを閉じるまで待機
trap "kill $SERVER_PID 2>/dev/null; echo 'サーバーを停止しました'" EXIT
wait $SERVER_PID
