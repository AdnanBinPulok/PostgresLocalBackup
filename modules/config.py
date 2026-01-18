"""Configuration management for PostgreSQL backup system."""
import json
import os
import pytz

# Timezone configuration
LOCAL_TIMEZONE = pytz.timezone('Asia/Dhaka')

# Root directory for backups
BACKUP_ROOT = 'backups'

# Backup retention limit per server
BACKUP_RETENTION_LIMIT = 5

# Backup schedule interval (in hours)
BACKUP_INTERVAL_HOURS = 1


async def get_servers():
    """
    Load server configurations from servers.json.
    
    Returns:
        list: List of server configuration dictionaries.
    """
    with open('./servers.json', 'r') as f:
        servers = json.load(f)
    return servers


def get_pg_dump_path():
    """
    Get the platform-specific path to pg_dump executable.
    
    Returns:
        str: Path to pg_dump executable.
    """
    if os.name == 'nt':
        # Windows path - adjust version number if needed
        return 'C:\\Program Files\\PostgreSQL\\17\\bin\\pg_dump.exe'
    else:
        # Unix-like systems (assumes pg_dump is in PATH)
        return 'pg_dump'
