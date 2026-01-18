"""Backup scheduling and orchestration."""
import asyncio
import schedule
import time
from datetime import datetime
from colorama import Fore

from modules.config import get_servers, LOCAL_TIMEZONE, BACKUP_INTERVAL_HOURS
from modules.backup import run_all_backups
from modules.cleanup import cleanup_all_servers
from modules.utils import format_time_duration


async def run_backup_cycle():
    """Execute a complete backup cycle: cleanup old backups, then create new ones."""
    servers = await get_servers()
    
    # Cleanup old backups first
    await cleanup_all_servers(servers)
    
    # Run backups for all servers
    await run_all_backups(servers)


def scheduled_backup():
    """Wrapper function for scheduled backup execution."""
    asyncio.run(run_backup_cycle())


def calculate_next_backup_time():
    """
    Calculate and display time until next scheduled backup.
    
    Returns:
        str: Formatted time until next backup, or None if not scheduled.
    """
    next_run = schedule.next_run()
    
    if not next_run:
        return None

    # Handle timezone awareness for schedule.next_run()
    if getattr(next_run, 'tzinfo', None) is None:
        try:
            next_run = LOCAL_TIMEZONE.localize(next_run)
        except Exception:
            next_run = next_run.replace(tzinfo=LOCAL_TIMEZONE)

    time_until_next = (next_run - datetime.now(LOCAL_TIMEZONE)).total_seconds()
    
    # Guard against negative values due to scheduling granularity
    if time_until_next < 0:
        time_until_next = 0

    return format_time_duration(time_until_next)


def start_scheduler():
    """
    Start the backup scheduler with configured interval.
    Runs indefinitely until interrupted.
    """
    schedule.every(BACKUP_INTERVAL_HOURS).hours.do(scheduled_backup)
    print(f"{Fore.GREEN}[*] Scheduler started. Backup interval: {BACKUP_INTERVAL_HOURS} hour(s)")

    # Display time until next backup
    next_backup_time = calculate_next_backup_time()
    if next_backup_time:
        print(f"{Fore.GREEN}[*] Next backup in: {next_backup_time}")

    # Run scheduler loop
    print(f"{Fore.GREEN}[*] Scheduler is now running. Press Ctrl+C to stop.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[*] Scheduler stopped by user")
