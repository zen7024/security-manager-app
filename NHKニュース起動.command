#!/bin/bash
# ダブルクリックするだけで起動します

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

echo "==============================="
echo "  三重県 NHK ニュース 起動中..."
echo "==============================="

# プロキシサーバーをバックグラウンドで起動
python3 "$DIR/nhk_proxy.py" &
PROXY_PID=$!

# 起動を待ってからブラウザを開く
sleep 1
open "$DIR/mie_nhk_news.html"

echo "✅ ブラウザが開きました"
echo ""
echo "このウィンドウを閉じるとサーバーも停止します。"
echo "（最小化したまま使い続けてください）"

# ウィンドウを閉じたらPythonも一緒に終了
trap "kill $PROXY_PID 2>/dev/null; echo ''; echo 'サーバーを停止しました。'" EXIT INT TERM

# サーバーが動いている間待機
wait $PROXY_PID
