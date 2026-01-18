"""Database backup operations."""
import os
import asyncio
from datetime import datetime
from colorama import Fore

from modules.config import BACKUP_ROOT, LOCAL_TIMEZONE, get_pg_dump_path


async def backup_database(server, db_name, timestamp_dir):
    """
    Backup a single database from a PostgreSQL server.
    
    Args:
        server (dict): Server configuration containing host, port, user, password, and name.
        db_name (str): Name of the database to backup.
        timestamp_dir (str): Directory path where the backup should be saved.
    """
    os.makedirs(timestamp_dir, exist_ok=True)
    filepath = os.path.join(timestamp_dir, f"{db_name}.sql")

    # Set password via environment variable
    env = os.environ.copy()
    env['PGPASSWORD'] = server['password']

    print(f"{Fore.CYAN}[→] Backing up {server['name']}/{db_name} to {filepath}")

    # Build pg_dump command
    command = [
        get_pg_dump_path(),
        '-h', server['host'],
        '-p', str(server['port']),
        '-U', server['user'],
        '-d', db_name,
        '-F', 'p',  # plain SQL format
        '-f', filepath
    ]

    try:
        process = await asyncio.create_subprocess_exec(
            *command,
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            print(f"{Fore.GREEN}[✓] Backup successful: {server['name']}/{db_name}")
        else:
            error_msg = stderr.decode().strip()
            print(f"{Fore.RED}[✗] Backup failed: {server['name']}/{db_name}\n{error_msg}")

    except FileNotFoundError as e:
        print(f"{Fore.YELLOW}[ERROR] pg_dump not found. Ensure it's in PATH. {e}")
    except Exception as e:
        print(f"{Fore.YELLOW}[ERROR] Exception during backup of {db_name} from {server['name']}: {e}")


async def backup_server(server):
    """
    Backup all databases from a single server concurrently.
    
    Args:
        server (dict): Server configuration containing databases list and connection details.
    """
    if not server.get('databases'):
        print(f"{Fore.YELLOW}[⚠] Skipping {server['name']}: No databases configured")
        return

    timestamp = datetime.now(LOCAL_TIMEZONE).strftime('%Y-%m-%d_%H-%M-%S')
    timestamp_dir = os.path.join(BACKUP_ROOT, server['name'], timestamp)

    print(f"{Fore.CYAN}[→] Starting backup for {server['name']} ({len(server['databases'])} databases)")

    tasks = [
        backup_database(server, db_name, timestamp_dir)
        for db_name in server['databases']
    ]

    await asyncio.gather(*tasks)
    print(f"{Fore.CYAN}[✓] Completed backup for {server['name']}")


async def run_all_backups(servers):
    """
    Run backups for all configured servers concurrently.
    
    Args:
        servers (list): List of server configurations.
    """
    print(f"{Fore.CYAN}[*] Starting backup for {len(servers)} server(s) at {datetime.now(LOCAL_TIMEZONE)}")
    
    tasks = [backup_server(server) for server in servers]
    await asyncio.gather(*tasks)
    
    print(f"{Fore.CYAN}[✓] All backups complete at {datetime.now(LOCAL_TIMEZONE)}")
