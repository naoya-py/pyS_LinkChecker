import asyncio
import aiohttp
import csv
import time
import sys

from html_report import csv_to_html

from rich.console import Console
from rich.table import Table
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TimeElapsedColumn,
    TextColumn,
)
import orjson
import pendulum
from pathlib import Path

URLS_TXT = 'samples/basic-urls/urls.txt'
REPORT_HTML = 'report.html'

# report CSV/JSON will be written to results/<run-timestamp>/
REPORTS_ROOT = Path('results')

# names for files (paths will be constructed per-run)
REPORT_CSV = 'report.csv'
REPORT_JSON = 'report.json'

console = Console()


async def fetch(session, url, sem, timeout=15):
    async with sem:
        start = time.time()
        try:
            async with session.get(url, timeout=timeout) as resp:
                status = resp.status
                reason = resp.reason if hasattr(resp, 'reason') else ''
                await resp.read()  # consume body
                elapsed = (time.time() - start) * 1000
                return {
                    'url': url,
                    'status': status,
                    'reason': reason,
                    'elapsed_ms': round(elapsed, 1),
                    'ok': 200 <= status < 400,
                }
        except asyncio.TimeoutError:
            return {
                'url': url,
                'status': 'TIMEOUT',
                'reason': 'timeout',
                'elapsed_ms': None,
                'ok': False,
            }
        except aiohttp.ClientResponseError as e:
            return {
                'url': url,
                'status': e.status if hasattr(e, 'status') else 'ERROR',
                'reason': str(e),
                'elapsed_ms': None,
                'ok': False,
            }
        except Exception as e:
            return {
                'url': url,
                'status': 'ERROR',
                'reason': str(e),
                'elapsed_ms': None,
                'ok': False,
            }


async def check_urls(urls, concurrency=10, timeout=15, console=None):
    sem = asyncio.Semaphore(concurrency)
    connector = aiohttp.TCPConnector(limit=concurrency)
    results = []
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch(session, u, sem, timeout) for u in urls]
        total = len(tasks)
        # show progress while awaiting tasks
        progress_console = console if console is not None else Console()
        with Progress(
            SpinnerColumn(),
            TextColumn('[progress.description]{task.description}'),
            BarColumn(),
            '[progress.percentage]{task.percentage:>3.0f}%',
            TimeElapsedColumn(),
            console=progress_console,
        ) as progress:
            task = progress.add_task('Checking URLs', total=total)
            for coro in asyncio.as_completed(tasks):
                r = await coro
                results.append(r)
                progress.advance(task)
    return results


def read_urls(path):
    urls = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith('#'):
                    continue
                urls.append(s)
    except FileNotFoundError:
        console.print(f"[red]{path} が見つかりません。サンプルの urls.txt を作成してください。[/red]")
        sys.exit(1)
    return urls


def write_csv(path, rows, checked_at):
    fieldnames = ['url', 'status', 'ok', 'reason', 'elapsed_ms', 'checked_at']
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            out = {k: r.get(k) for k in ['url', 'status', 'ok', 'reason', 'elapsed_ms']}
            out['checked_at'] = checked_at
            writer.writerow(out)


def write_json(path, rows, checked_at):
    # produce a JSON array where each item includes checked_at
    out_rows = []
    for r in rows:
        item = {k: r.get(k) for k in ['url', 'status', 'ok', 'reason', 'elapsed_ms']}
        item['checked_at'] = checked_at
        out_rows.append(item)
    # orjson returns bytes
    opts = getattr(orjson, 'OPT_INDENT_2', 0)
    # produce UTF-8 text for portability (write as text with encoding utf-8)
    data_bytes = orjson.dumps(out_rows, option=opts) if opts else orjson.dumps(out_rows)
    data_text = data_bytes.decode('utf-8')
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(data_text)
    # Also write a small metadata file recording the exact ISO timestamp used
    try:
        meta_path = Path(path).with_name('run_info.txt')
        with open(meta_path, 'w', encoding='utf-8') as mf:
            mf.write(f'run_timestamp: {checked_at}\n')
    except Exception:
        # non-fatal
        pass


def print_summary(rows):
    table = Table(title='リンクチェッカー結果')
    table.add_column('URL', overflow='fold')
    table.add_column('Status')
    table.add_column('OK')
    table.add_column('Elapsed(ms)')
    table.add_column('Reason', overflow='fold')
    ok_count = 0
    for r in rows:
        ok = r.get('ok')
        if ok:
            ok_count += 1
        table.add_row(
            r.get('url', ''),
            str(r.get('status', '')),
            str(r.get('ok', '')),
            str(r.get('elapsed_ms', '')),
            str(r.get('reason', '')),
        )
    console.print(table)
    console.print(f"Checked: {len(rows)}  OK: {ok_count}  NG: {len(rows)-ok_count}")


def main():
    console.print('[bold blue]リンクチェッカーを開始します[/bold blue]')
    urls = read_urls(URLS_TXT)
    if not urls:
        console.print('[yellow]チェックするURLがありません。urls.txt を確認してください。[/yellow]')
        return
    # create run timestamp with offset using pendulum
    run_time = pendulum.now('local')
    # ISO 8601 with offset, e.g. 2025-08-28T14:30:00+09:00
    iso_ts = run_time.to_iso8601_string()
    # sanitize for filesystem: replace ':' with '-' in dir name but keep ISO for metadata
    safe_ts = iso_ts.replace(':', '-')
    run_dir = REPORTS_ROOT / safe_ts
    run_dir.mkdir(parents=True, exist_ok=True)

    results = asyncio.run(check_urls(urls, console=console))
    csv_path = run_dir / REPORT_CSV
    json_path = run_dir / REPORT_JSON
    # use ISO timestamp with offset as checked_at
    checked_at = iso_ts
    write_csv(csv_path, results, checked_at)
    console.print(f'[green]CSV レポートを出力しました:[/green] {csv_path}')
    write_json(json_path, results, checked_at)
    console.print(f'[green]JSON レポートを出力しました:[/green] {json_path}')
    try:
        # HTML report stays at project root and references the CSV path
        csv_to_html(csv_path, REPORT_HTML)
        console.print(f'[green]HTML レポートを出力しました:[/green] {REPORT_HTML}')
    except Exception as e:
        console.print(f'[red]HTML 出力中にエラー:[/red] {e}')
    print_summary(results)


if __name__ == '__main__':
    main()