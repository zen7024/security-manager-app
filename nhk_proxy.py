#!/usr/bin/env python3
"""
NHK 三重県ニュース RSS プロキシサーバー
使い方: python3 nhk_proxy.py
ブラウザで mie_nhk_news.html を開いてください。
"""

import http.server
import urllib.request
import urllib.error
import json
import ssl
import gzip

# macOSのPythonはSSL証明書を自前で持たないため、検証をスキップする
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

PORT = 8765
RSS_URL = 'https://news.google.com/rss/search?q=%E4%B8%89%E9%87%8D%E7%9C%8C+NHK&hl=ja&gl=JP&ceid=JP:ja'

class ProxyHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/rss':
            self.fetch_rss()
        elif self.path == '/health':
            self.send_json({'status': 'ok'})
        else:
            self.send_response(404)
            self.end_headers()

    def fetch_rss(self):
        try:
            req = urllib.request.Request(
                RSS_URL,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Referer': 'https://www3.nhk.or.jp/lnews/tsu/',
                    'Connection': 'keep-alive',
                }
            )
            with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as response:
                raw = response.read()
                # gzip圧縮されている場合は解凍する
                if response.info().get('Content-Encoding') == 'gzip':
                    data = gzip.decompress(raw)
                else:
                    try:
                        data = gzip.decompress(raw)
                    except Exception:
                        data = raw

            self.send_response(200)
            self.send_header('Content-Type', 'application/xml; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')  # CORS許可
            self.end_headers()
            self.wfile.write(data)
            print(f'[OK] RSSを取得しました ({len(data)} bytes)')

        except urllib.error.URLError as e:
            print(f'[ERROR] RSSの取得失敗: {e}')
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

    def send_json(self, obj):
        body = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # ログを簡潔にする
        pass


if __name__ == '__main__':
    print('=' * 50)
    print('  NHK 三重県ニュース プロキシサーバー')
    print(f'  ポート: {PORT}')
    print('=' * 50)
    print('  ▶ mie_nhk_news.html をブラウザで開いてください')
    print('  ▶ 終了するには Ctrl+C を押してください')
    print('=' * 50)

    with http.server.HTTPServer(('localhost', PORT), ProxyHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print('\nサーバーを停止しました。')
