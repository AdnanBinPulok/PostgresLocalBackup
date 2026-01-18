# PostgreSQL Multi-Server Backup System

Automated backup solution for multiple PostgreSQL servers with scheduling and retention management.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Edit `servers.json` to configure your PostgreSQL servers:

```json
[
    {
        "name": "ServerName",
        "host": "192.168.1.100",
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

**Settings** (in `modules\config.py`):
- `BACKUP_RETENTION_LIMIT = 5` - Number of backups to keep per server
- `BACKUP_INTERVAL_HOURS = 1` - Hours between backups
- `LOCAL_TIMEZONE = pytz.timezone('Asia/Dhaka')` - Your timezone

## Usage

**Run the backup system:**
```bash
python main.py
```

This will:
1. Run an initial backup immediately
2. Delete old backups (keeps last 5)
3. Start the scheduler for periodic backups
4. Run continuously until stopped with `Ctrl+C`

## Backup Structure

```
backups/
└── ServerName/
    └── 2026-01-19_14-30-00/
        ├── database1.sql
        └── database2.sql
```

## Restoring a Backup

```bash
psql -h hostname -U postgres -d database_name -f "backups/ServerName/2026-01-19_14-30-00/database_name.sql"
```

## Common Issues

- **pg_dump not found** → Update path in `modules\config.py`
- **Connection refused** → Check host/port in `servers.json`
- **Authentication failed** → Verify username/password in `servers.json`
- **Server skipped** → Add databases to `"databases": []` array
