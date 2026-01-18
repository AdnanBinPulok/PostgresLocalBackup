"""Backup cleanup operations."""
import os
import shutil
from colorama import Fore

from modules.config import BACKUP_ROOT, BACKUP_RETENTION_LIMIT


async def delete_old_backups(server):
    """
    Delete old backup directories exceeding the retention limit.
    
    Args:
        server (dict): Server configuration containing the server name.
    """
    server_dir = os.path.join(BACKUP_ROOT, server['name'])
    
    if not os.path.exists(server_dir):
        return

    # Get all backup directories sorted by creation time (oldest first)
    backup_dirs = sorted(
        (os.path.join(server_dir, d) for d in os.listdir(server_dir) 
         if os.path.isdir(os.path.join(server_dir, d))),
        key=os.path.getctime
    )

    # Delete old backups if they exceed the retention limit
    while len(backup_dirs) > BACKUP_RETENTION_LIMIT - 1:
        old_backup = backup_dirs.pop(0)
        try:
            shutil.rmtree(old_backup)
            print(f"{Fore.YELLOW}[✓] Deleted old backup: {old_backup}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Failed to delete {old_backup}: {e}")


async def cleanup_all_servers(servers):
    """
    Clean up old backups for all configured servers.
    
    Args:
        servers (list): List of server configurations.
    """
    print(f"{Fore.RED}[*] Cleaning up old backups...")
    
    import asyncio
    delete_tasks = [delete_old_backups(server) for server in servers]
    await asyncio.gather(*delete_tasks)
    
    print(f"{Fore.GREEN}[✓] Cleanup complete")
