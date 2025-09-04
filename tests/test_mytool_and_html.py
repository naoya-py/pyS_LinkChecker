import csv

from html_report import csv_to_html

import Docstrings.mytool as dmy


def test_read_urls_and_csv_to_html(tmp_path):
    # create a sample CSV
    csv_file = tmp_path / 'report.csv'
    rows = [
        {
            'url': 'https://example.com',
            'status': '200',
            'ok': 'True',
            'reason': 'OK',
            'elapsed_ms': '100',
            'checked_at': '2025-09-04T10:00:00+09:00',
        },
        {
            'url': 'https://httpbin.org/status/404',
            'status': '404',
            'ok': 'False',
            'reason': 'NOT FOUND',
            'elapsed_ms': '50',
            'checked_at': '2025-09-04T10:00:00+09:00',
        },
    ]
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                'url',
                'status',
                'ok',
                'reason',
                'elapsed_ms',
                'checked_at',
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    html_file = tmp_path / 'report.html'
    csv_to_html(str(csv_file), str(html_file))

    assert html_file.exists()
    text = html_file.read_text(encoding='utf-8')
    assert 'https://example.com' in text
    assert 'tr class="ok"' in text
    assert 'https://httpbin.org/status/404' in text


def test_docstrings_importable():
    # ensure the documentation-only module is importable and has expected attributes
    assert hasattr(dmy, 'fetch')
    assert hasattr(dmy, 'check_urls')
    assert hasattr(dmy, 'write_csv')
    assert callable(dmy.fetch)
