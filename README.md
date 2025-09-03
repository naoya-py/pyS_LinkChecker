# URL ステータスチェッカー（リンクチェッカー）

[![python-3.12.10](https://img.shields.io/badge/python-3.12.10-brightgreen)](https://www.python.org/)
![status-prototype](https://img.shields.io/badge/status-prototype-yellow)

概要

- 指定した URL リスト（`urls.txt`）を非同期で巡回してステータスを確認します。

- 出力形式: CSV / JSON / HTML（すべて UTF-8 テキスト出力）

使い方（Windows / PowerShell）

1. 依存パッケージをインストール:

```powershell
python -m pip install -r requirements.txt
```

1. `urls.txt` にチェックしたい URL を 1 行ずつ記載します（`#` でコメント可能）。

1. 実行:

```powershell
python .\mytool.py
```

出力

- `report.csv` : URL ごとのステータスと応答時間を含む CSV（UTF-8）

- `report.json` : 同等データの JSON 配列（UTF-8 テキスト）

- `report.html` : 簡易な HTML レポート（`html_report.py` により生成）

依存

- aiohttp

- rich

- orjson

- requests（任意、将来の拡張用）

変更点（このバージョン）

- ターミナル出力を `rich` で装飾（進捗インジケータ、結果テーブル）

- JSON 出力を `orjson` を使って生成（UTF-8 テキストで出力）

- CSV / JSON ともに UTF-8 で出力するように変更

注意

- 実行前に `requirements.txt` に記載のパッケージをインストールしてください。

- orjson は OS / Python バージョンによってビルドが必要な場合があります。Windows 環境で問題が出る場合は `pip` のエラーメッセージに従ってください。

拡張案

- CLI で並列度・タイムアウト・出力形式を指定可能にする

- 各 URL の応答時刻（個別 checked_at）を記録する

- 再試行・レート制御・認証ヘッダのサポート

ライセンス / 貢献

- 必要ならリポジトリに LICENSE を追加してください（現状は未指定）。

---

簡単な確認手順（PowerShell）

```powershell
cd path\to\pyS_LinkChecker
python -m pip install -r requirements.txt
python .\mytool.py
```

生成された `report.csv` / `report.json` / `report.html` をブラウザやエディタで確認してください。

ご希望があれば README にバッジ（CI・PyPI・License 等）を追加します。現在は最小のバッジを上部に追加しています。
