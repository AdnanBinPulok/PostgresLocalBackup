"""Utility functions for the backup system."""


def format_time_duration(seconds):
    """
    Convert seconds to human-readable duration format.
    
    Args:
        seconds (float): Duration in seconds.
    
    Returns:
        str: Formatted duration string (e.g., "1 day, 2 hours, 3 minutes").
    
    Example:
        >>> format_time_duration(90061)
        '1 day, 1 hour, 1 minute, 1 second'
    """
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    time_parts = []
    if days > 0:
        time_parts.append(f"{round(days, 1)} day{'s' if days > 1 else ''}")
    if hours > 0:
        time_parts.append(f"{round(hours, 1)} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        time_parts.append(f"{round(minutes, 1)} minute{'s' if minutes > 1 else ''}")
    if seconds > 0:
        time_parts.append(f"{round(seconds, 1)} second{'s' if seconds > 1 else ''}")

    return ', '.join(time_parts) if time_parts else '0 seconds'
