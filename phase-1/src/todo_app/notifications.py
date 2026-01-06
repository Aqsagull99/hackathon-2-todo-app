"""Notification system for task reminders with cross-platform support."""
import subprocess
import platform


class NotificationManager:
    """Handles sending system notifications for task reminders.

    Provides platform-specific implementations with graceful fallback
    to console output when system notifications are not available.
    """

    def __init__(self):
        """Initialize notification manager and detect platform."""
        self.platform = platform.system().lower()

    def send_notification(self, title: str, message: str) -> bool:
        """Send a system notification if available, fallback to console.

        Args:
            title: Notification title (e.g., task name)
            message: Notification message (e.g., due time)

        Returns:
            True if notification was sent (system or console), False on error
        """
        try:
            if self.platform == 'linux':
                return self._notify_linux(title, message)
            elif self.platform == 'darwin':
                return self._notify_macos(title, message)
            elif self.platform == 'windows':
                return self._notify_windows(title, message)
            else:
                # Unknown platform, fallback to console
                return self._notify_console(title, message)
        except Exception:
            # Any error, fallback to console
            return self._notify_console(title, message)

    def _notify_linux(self, title: str, message: str) -> bool:
        """Send notification on Linux using notify-send.

        Args:
            title: Notification title
            message: Notification message

        Returns:
            True if sent, False on failure
        """
        cmd = ["notify-send", "-u", "normal", title, message]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return self._notify_console(title, message)
        return True

    def _notify_macos(self, title: str, message: str) -> bool:
        """Send notification on macOS using osascript.

        Args:
            title: Notification title
            message: Notification message

        Returns:
            True (macOS always has osascript)
        """
        cmd = [
            "osascript", "-e",
            f'display notification "{message}" with title "{title}"'
        ]
        subprocess.run(cmd, capture_output=True, text=True)
        return True

    def _notify_windows(self, title: str, message: str) -> bool:
        """Send notification on Windows using PowerShell.

        Args:
            title: Notification title
            message: Notification message

        Returns:
            True (Windows always has PowerShell)
        """
        powershell_script = f"""
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.ToolTip]::new().Show("{message}", "{title}", 0, 0, 5000)
        """
        cmd = ["powershell", "-Command", powershell_script]
        subprocess.run(cmd, capture_output=True, text=True)
        return True

    def _notify_console(self, title: str, message: str) -> bool:
        """Fallback: Print reminder to console with visual indicator.

        Args:
            title: Notification title
            message: Notification message

        Returns:
            True (console output always succeeds)
        """
        try:
            print(f"\n🔔 REMINDER: [{title}] {message}")
        except UnicodeEncodeError:
            # Fallback for terminals that don't support emoji
            print(f"\n[!] REMINDER: [{title}] {message}")
        print("Press Enter to continue...")
        return True
