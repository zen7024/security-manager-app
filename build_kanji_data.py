#!/usr/bin/env python3
# ============================================================
# 漢字辞典データベース生成スクリプト
# build_kanji_data.py
#
# 使い方:
#   1. このファイルを「漢字辞典.html」と同じフォルダに置く
#   2. ターミナルで以下を実行:
#      python3 build_kanji_data.py
#   3. 完了すると 漢字辞典.html が自動更新される
#
# ネット接続が必要です（KANJIDIC2をダウンロードします）
# ============================================================

import urllib.request
import gzip
import xml.etree.ElementTree as ET
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE  = os.path.join(SCRIPT_DIR, "漢字辞典.html")
KANJIDIC2_URL = "http://www.edrdg.org/kanjidic/kanjidic2.xml.gz"
KANJIDIC2_GZ  = os.path.join(SCRIPT_DIR, "kanjidic2.xml.gz")
KANJIDIC2_XML = os.path.join(SCRIPT_DIR, "kanjidic2.xml")

# ---- Step 1: ダウンロード ----
def download_kanjidic2():
    if os.path.exists(KANJIDIC2_XML):
        print("✅ kanjidic2.xml は既にあります。スキップします。")
        return
    print("📥 KANJIDIC2 をダウンロード中... (約 10MB、少し時間がかかります)")
    try:
        urllib.request.urlretrieve(KANJIDIC2_URL, KANJIDIC2_GZ)
        print("📦 解凍中...")
        with gzip.open(KANJIDIC2_GZ, 'rb') as f_in:
            with open(KANJIDIC2_XML, 'wb') as f_out:
                f_out.write(f_in.read())
        os.remove(KANJIDIC2_GZ)
        print("✅ ダウンロード完了!")
    except Exception as e:
        print(f"❌ ダウンロード失敗: {e}")
        print("  → ネット接続を確認してください。")
        sys.exit(1)

# ---- Step 2: XML解析して画数→漢字リストを作成 ----
def parse_kanjidic2():
    print("🔍 KANJIDIC2 を解析中... (数千件、少し時間がかかります)")
    stroke_map = {}  # {画数: [漢字, ...]}

    tree = ET.parse(KANJIDIC2_XML)
    root = tree.getroot()

    count = 0
    for character in root.findall('character'):
        # 漢字本体
        literal = character.find('literal')
        if literal is None:
            continue
        kanji = literal.text

        # 画数を取得
        misc = character.find('misc')
        if misc is None:
            continue
        stroke_count_elem = misc.find('stroke_count')
        if stroke_count_elem is None:
            continue

        try:
            sc = int(stroke_count_elem.text)
        except:
            continue

        if sc not in stroke_map:
            stroke_map[sc] = []
        stroke_map[sc].append(kanji)
        count += 1

    print(f"✅ {count} 文字を読み込みました。")
    return stroke_map

# ---- Step 3: JS形式の文字列を生成 ----
def build_sc_js(stroke_map):
    lines = []
    lines.append("// ★自動生成 by build_kanji_data.py (KANJIDIC2より)")
    lines.append("const SC = {")
    for sc in sorted(stroke_map.keys()):
        chars = "".join(stroke_map[sc])
        # JSのコードとしてエスケープ不要（UTF-8そのまま）
        lines.append(f'  {sc}: "{chars}",')
    lines.append("};")
    return "\n".join(lines)

# ---- Step 4: HTMLファイルのSCブロックを置き換え ----
def update_html(sc_js):
    if not os.path.exists(HTML_FILE):
        print(f"❌ 漢字辞典.html が見つかりません: {HTML_FILE}")
        sys.exit(1)

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    # SCオブジェクトのブロックを検索して置換
    # パターン: // ★自動生成... または const SC = { で始まり }; で終わるブロック
    pattern = r'(// ★自動生成 by build_kanji_data\.py.*?\n)?const SC = \{.*?\n\};'

    new_html = re.sub(pattern, sc_js, html, flags=re.DOTALL)

    if new_html == html:
        # パターンが見つからない場合、古い形式のSCを探す
        pattern2 = r'const SC = \{[^}]*(?:\{[^}]*\}[^}]*)?\};'
        new_html = re.sub(pattern2, sc_js, html, flags=re.DOTALL)

    if new_html == html:
        print("⚠️  HTMLファイルのSCブロックが見つかりませんでした。")
        print("   手動で sc_output.js の内容をHTMLに貼り付けてください。")
        # フォールバック: JSファイルとして出力
        js_file = os.path.join(SCRIPT_DIR, "sc_output.js")
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(sc_js)
        print(f"   → {js_file} に出力しました。")
        return False

    # バックアップを作成
    backup = HTML_FILE + ".bak"
    with open(backup, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"💾 バックアップ: 漢字辞典.html.bak")

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_html)

    return True

# ---- Step 5: 統計を表示 ----
def show_stats(stroke_map):
    total = sum(len(v) for v in stroke_map.values())
    print(f"\n📊 データベース統計:")
    print(f"   総文字数: {total:,}")
    print(f"   画数範囲: {min(stroke_map.keys())} 〜 {max(stroke_map.keys())} 画")
    print(f"\n   画数別件数 (上位10):")
    sorted_by_count = sorted(stroke_map.items(), key=lambda x: len(x[1]), reverse=True)
    for sc, chars in sorted_by_count[:10]:
        print(f"     {sc:2d}画: {len(chars):4d}文字")

# ---- メイン ----
def main():
    print("=" * 50)
    print(" 漢字辞典 DB生成スクリプト")
    print("=" * 50)

    download_kanjidic2()
    stroke_map = parse_kanjidic2()
    show_stats(stroke_map)

    print("\n✏️  HTMLファイルを更新中...")
    sc_js = build_sc_js(stroke_map)
    success = update_html(sc_js)

    if success:
        print("✅ 漢字辞典.html のデータベースを更新しました！")
        print("\n🎉 完了！ブラウザで漢字辞典.html を開き直してください。")

    # 一時ファイルのクリーンアップ確認
    if os.path.exists(KANJIDIC2_XML):
        size_mb = os.path.getsize(KANJIDIC2_XML) / 1024 / 1024
        print(f"\n💡 kanjidic2.xml ({size_mb:.1f}MB) は削除しても構いません。")
        print("   次回また実行する場合は残しておくとダウンロードをスキップできます。")

if __name__ == "__main__":
    main()
