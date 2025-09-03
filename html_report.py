import csv

HTML_TEMPLATE = '''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>リンクチェッカー レポート</title>
  <style>
    body{font-family:Segoe UI,Arial,Helvetica,sans-serif;padding:20px}
    table{border-collapse:collapse;width:100%}
    th,td{border:1px solid #ddd;padding:8px;text-align:left}
    th{background:#f5f5f5}
    tr.ok td{background:#eef9ee}
    tr.ng td{background:#fdecea}
  </style>
</head>
<body>
  <h1>リンクチェッカー レポート</h1>
  <p>生成日時: {generated}</p>
  <table>
    <thead>
      <tr>
        <th>URL</th>
        <th>ステータス</th>
        <th>OK</th>
        <th>理由</th>
        <th>応答時間(ms)</th>
        <th>チェック日時</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
</body>
</html>
'''

ROW_TEMPLATE = '<tr class="{cls}"><td><a href="{url}" target="_blank">{url}</a></td><td>{status}</td><td>{ok}</td><td>{reason}</td><td>{elapsed}</td><td>{checked_at}</td></tr>'

def csv_to_html(csv_path, out_path):
    rows_html = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            ok = r.get('ok', '')
            cls = 'ok' if ok.lower() in ('true', '1') else 'ng'
            rows_html.append(ROW_TEMPLATE.format(
                cls=cls,
                url=r.get('url',''),
                status=r.get('status',''),
                ok=r.get('ok',''),
                reason=r.get('reason',''),
                elapsed=r.get('elapsed_ms',''),
                checked_at=r.get('checked_at','')
            ))
    html = HTML_TEMPLATE.format(generated='', rows='\n'.join(rows_html))
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
