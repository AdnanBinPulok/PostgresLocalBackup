"""PostgreSQL Multi-Server Backup System - Main Entry Point."""
import asyncio
from colorama import init, Fore

from modules.scheduler import run_backup_cycle, start_scheduler

# Initialize colorama for colored console output
init(autoreset=True)


def main():
    """Main entry point for the backup system."""
    print(f"{Fore.YELLOW}[*] PostgreSQL Backup System Starting...")
    
    # Run initial backup immediately
    print(f"{Fore.YELLOW}[*] Running initial backup...")
    asyncio.run(run_backup_cycle())
    print(f"{Fore.YELLOW}[*] Initial backup complete.")

    # Start the scheduler for periodic backups
    start_scheduler()


if __name__ == "__main__":
    main()
