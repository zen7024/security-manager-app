# 📖 漢字辞典

難解漢字・古来漢字に特化した手書き対応の漢字辞典アプリです。
インストール不要で、ブラウザだけで動作します。

---

## ✨ 機能

- **✍️ 手書き検索** — 指やマウスで漢字を書いて検索（Google AIによる形状認識）
- **🔍 読み検索** — ひらがな・カタカナで読みを入力して検索
- **📚 難読・古字タブ** — 難読漢字・古来漢字をカテゴリ別に一覧表示
- **⭐ お気に入り** — よく調べる漢字をブックマーク保存
- **13,000字以上のデータベース** — KANJIDIC2による充実した漢字データ

---

## 📱 使い方

### Androidで使う（インストール不要）

1. `漢字辞典.html` をAndroidに転送する（メール・AirDrop等）
2. Chrome で開く

> ⚠️ `file://` で開いた場合、手書き認識はGoogle AIではなく画数ベースになります。

---

### Macで使う（Google AI形状認識が有効になる）

1. `漢字辞典を起動.command` をダブルクリック
2. ブラウザが自動で開きます（`http://localhost:8765`）

> 初回は「開発元が未確認」と出る場合があります。
> Finder で右クリック →「開く」→「開く」で起動できます。

---

## 📂 ファイル構成

```
漢字辞典.html          # アプリ本体（これ1つで動く）
漢字辞典を起動.command  # Mac用ランチャー（localhost経由で起動）
build_kanji_data.py    # データベース充実化スクリプト
```

---

## 🗄️ データベースを充実させる

`build_kanji_data.py` を実行すると、KANJIDIC2から13,000字以上の漢字データを自動取得し、アプリに組み込みます。

```bash
# 漢字辞典.html と同じフォルダで実行
python3 build_kanji_data.py
```

- ネット接続が必要です（初回のみ約10MBダウンロード）
- 完了後は `漢字辞典.html` を開き直すだけで反映されます

---

## 🛠️ 技術情報

| 項目 | 詳細 |
|------|------|
| 動作環境 | Android Chrome / Mac Chrome / Safari |
| 手書き認識 | [Google Handwriting Input API](https://inputtools.google.com)（HTTP経由のみ） |
| 漢字情報 | [kanjiapi.dev](https://kanjiapi.dev) / [jisho.org](https://jisho.org) |
| データベース | [KANJIDIC2](http://www.edrdg.org/wiki/index.php/KANJIDIC_Project) |
| 保存 | localStorage（お気に入り） |
| 依存ライブラリ | なし（単一HTMLファイル） |

---

## 📝 ライセンス

個人利用・非商用に限り自由に使用できます。
KANJIDIC2のデータは [Electronic Dictionary Research and Development Group](http://www.edrdg.org/) のライセンスに従います。
