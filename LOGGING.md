# Game Logging System

The Stupid Duck game now includes comprehensive error logging to help track and debug issues.

## Log Files

When you run the game, two log files are created in the `logs/` directory:

1. **`game_YYYYMMDD_HHMMSS.log`** - Complete game log with all messages (DEBUG, INFO, WARNING, ERROR, CRITICAL)
2. **`errors_YYYYMMDD_HHMMSS.log`** - Errors and critical issues only

## Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages (game starting, saving, etc.)
- **WARNING**: Warning messages (non-critical issues)
- **ERROR**: Errors that occurred but didn't crash the game
- **CRITICAL**: Severe errors that may have caused a crash

## Viewing Logs

### Using the view_logs.py script:

```bash
# View latest 50 lines
python view_logs.py latest

# View all logs
python view_logs.py all

# View errors only
python view_logs.py errors

# View last 100 lines
python view_logs.py latest -n 100

# List all log files
python view_logs.py list
```

### Manual viewing:

```bash
# View the latest game log
tail -f logs/game_*.log

# View the latest error log
tail -f logs/errors_*.log

# View all errors
cat logs/errors_*.log
```

## What Gets Logged

- Game startup and shutdown
- Fatal errors and crashes
- Exception stack traces
- User interrupts (Ctrl+C)
- Critical system issues

## Log Cleanup

Log files can accumulate over time. To clean up old logs:

```bash
# Remove logs older than 7 days
find logs/ -name "*.log" -mtime +7 -delete

# Remove all logs
rm -rf logs/
```

## Privacy Note

Logs contain game state information but no personal data. They're stored locally and never transmitted anywhere.

## Troubleshooting

If you encounter an error:

1. Check the latest error log: `python view_logs.py errors`
2. Look for the stack trace and error message
3. The log includes the filename and line number where the error occurred

## Log Rotation

Logs are automatically rotated - a new log file is created each time you start the game. This prevents log files from growing too large.
