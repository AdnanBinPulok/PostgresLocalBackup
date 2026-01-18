# PostgreSQL Multi-Server Backup System

Automated backup solution for multiple PostgreSQL servers with retention management and scheduling.

## Features

- ✅ **Multi-Server Support**: Backup multiple PostgreSQL servers concurrently
- ✅ **Automatic Retention**: Maintains configurable number of backup copies per server
- ✅ **Scheduled Backups**: Runs backups at configurable intervals
- ✅ **Concurrent Execution**: Parallel backup execution for faster completion
- ✅ **Colored Output**: Easy-to-read console output with status indicators
- ✅ **Error Handling**: Robust error handling with detailed logging

## Project Structure

```
├── main.py           # Entry point - orchestrates the backup system
├── config.py         # Configuration management (servers, paths, settings)
├── backup.py         # Database backup operations
├── cleanup.py        # Old backup cleanup operations
├── scheduler.py      # Backup scheduling logic
├── utils.py          # Utility functions (time formatting, etc.)
├── servers.json      # Server configuration file
└── requirements.txt  # Python dependencies
```

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your PostgreSQL servers in `servers.json`:
```json
[
    {
        "name": "ServerName",
        "host": "hostname_or_ip",
        "port": 5432,
        "user": "postgres",
        "password": "your_password",
        "databases": [
            "database1",
            "database2"
        ]
    }
]
```

3. Adjust settings in `config.py` if needed:
   - `BACKUP_RETENTION_LIMIT`: Number of backups to keep per server (default: 5)
   - `BACKUP_INTERVAL_HOURS`: Hours between scheduled backups (default: 1)
   - `LOCAL_TIMEZONE`: Your local timezone (default: Asia/Dhaka)

## Usage

Run the backup system:
```bash
python main.py
```

The system will:
1. Run an initial backup immediately
2. Start the scheduler for periodic backups
3. Clean up old backups automatically

## Configuration

### Timezone Settings
Edit `LOCAL_TIMEZONE` in `config.py`:
```python
LOCAL_TIMEZONE = pytz.timezone('Asia/Dhaka')
```

### Backup Retention
Edit `BACKUP_RETENTION_LIMIT` in `config.py`:
```python
BACKUP_RETENTION_LIMIT = 5  # Keep last 5 backups per server
```

### Backup Interval
Edit `BACKUP_INTERVAL_HOURS` in `config.py`:
```python
BACKUP_INTERVAL_HOURS = 1  # Backup every 1 hour
```

### PostgreSQL Path (Windows)
Edit `get_pg_dump_path()` in `config.py` if your PostgreSQL is installed in a different location:
```python
return 'C:\\Program Files\\PostgreSQL\\17\\bin\\pg_dump.exe'
```

## Backup Structure

Backups are organized as follows:
```
backups/
├── ServerName1/
│   ├── 2026-01-18_12-00-00/
│   │   ├── database1.sql
│   │   └── database2.sql
│   └── 2026-01-18_13-00-00/
│       ├── database1.sql
│       └── database2.sql
└── ServerName2/
    └── 2026-01-18_12-00-00/
        └── database1.sql
```

## Module Details

### `config.py`
- Server configuration loading
- Path management
- Global settings

### `backup.py`
- Individual database backup
- Server-level backup orchestration
- Concurrent backup execution

### `cleanup.py`
- Old backup detection
- Retention policy enforcement
- Safe deletion with error handling

### `scheduler.py`
- Backup cycle orchestration
- Scheduling logic
- Next backup time calculation

### `utils.py`
- Time duration formatting
- Helper functions

## Requirements

- Python 3.7+
- PostgreSQL (pg_dump must be accessible)
- Required Python packages (see requirements.txt):
  - colorama
  - schedule
  - pytz

## Troubleshooting

**Issue**: `pg_dump not found`
- Ensure PostgreSQL is installed
- Update `get_pg_dump_path()` in `config.py` with correct path

**Issue**: Connection refused
- Verify server host, port, and credentials in `servers.json`
- Ensure PostgreSQL server is running and accessible

**Issue**: Permission denied
- Check database user permissions
- Ensure write permissions in backup directory

## License

MIT License
