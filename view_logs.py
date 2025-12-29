#!/usr/bin/env python3
"""
View game logs - displays the latest log files.
"""
import sys
from pathlib import Path
import argparse


def view_logs(log_type='all', tail=50):
    """
    View game logs.

    Args:
        log_type: 'all', 'errors', or 'latest'
        tail: Number of lines to show from the end
    """
    logs_dir = Path(__file__).parent / "logs"

    if not logs_dir.exists():
        print("No logs directory found. Run the game first to generate logs.")
        return

    # Find latest log files
    all_logs = sorted(logs_dir.glob("game_*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    error_logs = sorted(logs_dir.glob("errors_*.log"), key=lambda p: p.stat().st_mtime, reverse=True)

    if not all_logs:
        print("No log files found.")
        return

    latest_game_log = all_logs[0]
    latest_error_log = error_logs[0] if error_logs else None

    print("=" * 80)
    print("STUPID DUCK - GAME LOGS")
    print("=" * 80)
    print(f"Latest game log: {latest_game_log.name}")
    if latest_error_log:
        print(f"Latest error log: {latest_error_log.name}")
    print("=" * 80)
    print()

    if log_type == 'errors' and latest_error_log:
        print("ERRORS ONLY:")
        print("-" * 80)
        try:
            with open(latest_error_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if tail > 0:
                    lines = lines[-tail:]
                print(''.join(lines))
        except Exception as e:
            print(f"Error reading error log: {e}")

    elif log_type == 'all':
        print("ALL LOGS:")
        print("-" * 80)
        try:
            with open(latest_game_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if tail > 0:
                    lines = lines[-tail:]
                print(''.join(lines))
        except Exception as e:
            print(f"Error reading log: {e}")

    elif log_type == 'latest':
        print("LATEST ENTRIES:")
        print("-" * 80)
        try:
            with open(latest_game_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(''.join(lines[-tail:]))
        except Exception as e:
            print(f"Error reading log: {e}")


def list_logs():
    """List all available log files."""
    logs_dir = Path(__file__).parent / "logs"

    if not logs_dir.exists():
        print("No logs directory found.")
        return

    all_logs = sorted(logs_dir.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)

    if not all_logs:
        print("No log files found.")
        return

    print("=" * 80)
    print("AVAILABLE LOG FILES")
    print("=" * 80)

    for log_file in all_logs:
        size_kb = log_file.stat().st_size / 1024
        modified = log_file.stat().st_mtime
        import datetime
        mod_time = datetime.datetime.fromtimestamp(modified).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{log_file.name:<30} {size_kb:>8.1f} KB  {mod_time}")


def main():
    parser = argparse.ArgumentParser(description='View Stupid Duck game logs')
    parser.add_argument(
        'action',
        nargs='?',
        default='latest',
        choices=['all', 'errors', 'latest', 'list'],
        help='What to view: all logs, errors only, latest entries, or list files'
    )
    parser.add_argument(
        '-n', '--lines',
        type=int,
        default=50,
        help='Number of lines to show (default: 50)'
    )

    args = parser.parse_args()

    if args.action == 'list':
        list_logs()
    else:
        view_logs(args.action, args.lines)


if __name__ == "__main__":
    main()
