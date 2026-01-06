"""User-friendly interactive menu-based UI for todo application using Rich and Console I/O Skill patterns."""
import sys
import tty
import termios
from typing import Optional, List
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live
from rich.box import DOUBLE_EDGE, ROUNDED, ASCII

from .storage import TaskList
from .models import Task, Priority, Recurrence


class InteractiveUI:
    """Interactive UI with arrow key support and Rich terminal-style layout."""

    def __init__(self, tasklist: TaskList) -> None:
        self.tasklist = tasklist
        self.console = Console()
        self.width = 60

    # ==================== SCREEN DRAWING ====================

    def clear_screen(self) -> None:
        """Clear the terminal screen forcefully."""
        # \033[H moves cursor to top-left, \033[J clears from cursor to end of screen
        print("\033[H\033[J", end="")
        self.console.clear()

    def print_banner(self) -> None:
        """Print the evolution banner using Rich Panel."""
        banner_text = Text("THE EVOLUTION OF TODO", style="bold magenta", justify="center")
        self.console.print(
            Panel(
                banner_text,
                box=DOUBLE_EDGE,
                border_style="magenta",
                width=self.width,
                padding=(1, 2)
            )
        )

    def print_header(self, title: str) -> None:
        """Print a header box using Rich."""
        self.console.print(
            Panel(
                Text(title, style="bold cyan", justify="center"),
                box=ROUNDED,
                border_style="cyan",
                width=self.width
            )
        )

    def print_info(self, message: str) -> None:
        """Print an informational message."""
        self.console.print(f" [bold blue]ℹ[/bold blue] {message}")

    def print_success(self, message: str) -> None:
        """Print a success message."""
        self.console.print(f" [bold green]✓[/bold green] {message}")

    def print_error(self, message: str) -> None:
        """Print an error message."""
        self.console.print(f" [bold red]✗[/bold red] {message}")

    def get_menu_renderable(self, options: list, selected: int = 0) -> Panel:
        """Create a single renderable containing banner and menu."""
        menu_content = Text()
        menu_content.append("\n VIEW & MANAGE TASKS\n", style="bold white")
        menu_content.append(" ──────────────────────────────\n\n", style="dim")

        for i, opt in enumerate(options):
            if i == selected:
                menu_content.append("  ➜  ", style="bold yellow")
                menu_content.append(f"{i + 1}. {opt}", style="bold reverse magenta")
            else:
                menu_content.append(f"     {i + 1}. {opt}", style="white")

            if i < len(options) - 1:
                menu_content.append("\n")

        return Panel(
            menu_content,
            box=ROUNDED,
            border_style="purple",
            width=self.width,
            subtitle="[dim]Use ↑/↓ arrows to navigate, Enter to select[/dim]"
        )

    def draw_menu(self, options: list, selected: int = 0) -> None:
        """Legacy draw_menu for static parts."""
        self.clear_screen()
        self.print_banner()
        self.console.print(self.get_menu_renderable(options, selected))

    def get_task_list_renderable(self, tasks: list, selected: int = 0, mode: str = "view") -> Panel:
        """Create a single renderable containing task table."""
        if not tasks:
            return Panel(
                Text("\nNo tasks yet! Add a task to get started.\n", justify="center"),
                title="YOUR TASKS",
                border_style="yellow",
                width=self.width
            )

        table = Table(box=None, header_style="bold cyan", width=self.width - 4, show_header=True)
        table.add_column("  #", width=6)
        table.add_column("STATUS", width=12)
        table.add_column("PRI", width=4)
        table.add_column("TASK")
        table.add_column("TAGS", width=12, justify="right")

        for i, task in enumerate(tasks):
            style = "bold magenta" if i == selected else ""
            marker = "▶ " if i == selected else "  "

            status = Text("DONE", style="bold green") if task.completed else Text("PENDING", style="bold yellow")

            # Priority indicator
            priority_char = "H" if task.priority == Priority.HIGH else "M" if task.priority == Priority.MEDIUM else "L"
            priority_style = "bold red" if task.priority == Priority.HIGH else "yellow" if task.priority == Priority.MEDIUM else "green"
            priority_text = Text(priority_char, style=priority_style)

            # Tags display
            tags_str = ",".join(task.tags[:2]) if task.tags else ""
            tags_text = Text(tags_str, style="cyan") if tags_str else Text("", style="dim")

            table.add_row(
                Text(f"{marker}{task.id}", style=style),
                status,
                priority_text,
                Text(task.title, style=style),
                tags_text
            )

        footer_text = ""
        if mode == "select":
            footer_text = " ↑/↓ navigate  •  ENTER select task  •  q go back"
        else:
            footer_text = " c complete  •  d delete  •  e edit  •  q go back"

        return Panel(
            table,
            border_style="purple",
            width=self.width,
            title="TASK LIST",
            subtitle=f"[dim]{footer_text}[/dim]"
        )

    def draw_task_list(self, tasks: list, selected: int = 0, mode: str = "view") -> None:
        """Legacy draw_task_list for static parts."""
        self.clear_screen()
        self.print_header("VIEW & MANAGE TASKS")
        print()
        self.console.print(self.get_task_list_renderable(tasks, selected, mode))

    # ==================== KEYBOARD INPUT ====================

    def get_key(self) -> str:
        """Read a single keypress, handling arrow keys."""
        fd = sys.stdin.fileno()
        try:
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                key = sys.stdin.read(1)
                if key == '\x1b':  # ESC sequence
                    seq = sys.stdin.read(2)
                    if seq == '[A':
                        return 'UP'
                    elif seq == '[B':
                        return 'DOWN'
                return key
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except termios.error:
            # Fallback for non-interactive environments
            # Just read a regular character
            return sys.stdin.read(1)

    def get_yes_no(self, question: str) -> bool:
        """Get yes/no confirmation."""
        try:
            self.console.print(f"\n [bold yellow]?[/bold yellow] {question} (y/n): ", end="")
            while True:
                response = sys.stdin.read(1).lower()
                if response in ['y', 'n']:
                    print(response)
                    return response == 'y'
        except:
            # Fallback for environments where stdin.read(1) doesn't work
            while True:
                response = input(f"\n{question} (y/n): ").strip().lower()
                if response in ['y', 'n']:
                    return response == 'y'

    def press_enter_to_continue(self) -> None:
        """Wait for user to press Enter."""
        self.console.print("\n [dim]Press Enter to continue...[/dim]")
        try:
            sys.stdin.read(1)
        except:
            # Fallback if stdin is not available
            input()

    # ==================== MAIN APPLICATION LOOP ====================

    def run(self) -> None:
        """Run the main application loop using the alternate screen buffer for a static experience."""
        selected = 0
        options = [
            "Add New Task",
            "View Tasks",
            "Update Task",
            "Mark as Complete",
            "Delete Task",
            "Set Priority",
            "Set Due Date",
            "Manage Tags",
            "Search Tasks",
            "Check Reminders",
            "Exit Application"
        ]

        # Try to use screen buffer (for interactive terminals), fall back to regular output if not available
        try:
            with Live(console=self.console, auto_refresh=False, screen=True) as live:
                while True:
                    # Build the layout manually for the live update
                    full_menu = Text()
                    # Repurpose draw_menu parts to build a single renderable
                    banner_text = Text("\nTHE EVOLUTION OF TODO\n", style="bold magenta", justify="center")
                    banner_panel = Panel(banner_text, box=DOUBLE_EDGE, border_style="magenta", width=self.width)

                    menu_renderable = self.get_menu_renderable(options, selected)

                    # Create a layout-like structure
                    from rich.console import Group
                    display_group = Group(banner_panel, menu_renderable)

                    live.update(display_group, refresh=True)

                    key = self.get_key()

                    if key in ['\r', '\n']:  # Enter
                        # We need to temporarily leave the live screen to handle prompts
                        live.stop()
                        if selected == 0:
                            self.handle_add_task()
                        elif selected == 1:
                            self.handle_view_tasks()
                        elif selected == 2:
                            self.handle_update_task()
                        elif selected == 3:
                            self.handle_mark_complete()
                        elif selected == 4:
                            self.handle_delete_by_id()
                        elif selected == 5:
                            self.handle_set_priority()
                        elif selected == 6:
                            self.handle_set_due_date()
                        elif selected == 7:
                            self.handle_manage_tags()
                        elif selected == 8:
                            self.handle_search_tasks()
                        elif selected == 9:
                            self.handle_check_reminders()
                        elif selected == 10:  # Exit Application
                            # Exit the app with farewell message
                            self.clear_screen()
                            self.console.print("\n👋 Thank you for using the Todo App! See you soon.\n", style="bold green")
                            break
                        else:
                            break
                        # Re-enter alternate screen buffer
                        live.start()
                    elif key == 'UP':
                        selected = (selected - 1) % len(options)
                    elif key == 'DOWN':
                        selected = (selected + 1) % len(options)
                    elif key.lower() == 'q':
                        # Exit the app with farewell message
                        self.clear_screen()
                        self.console.print("\n👋 Thank you for using the Todo App! See you soon.\n", style="bold green")
                        break
        except Exception:
            # Fallback to a simpler menu system when screen buffer isn't available
            while True:
                self.clear_screen()
                self.print_banner()
                print()

                # Display menu options
                for i, option in enumerate(options, 1):
                    if i-1 == selected:
                        print(f"  ➜  {i}. {option}")
                    else:
                        print(f"     {i}. {option}")

                print(f"\nUse numbers to select, 'q' to quit")

                try:
                    choice = input("\nEnter choice (1-10) or 'q' to quit: ").strip().lower()

                    if choice == 'q':
                        print("👋 Thank you for using the Todo App! See you soon.\n")
                        break
                    elif choice.isdigit():
                        choice_num = int(choice) - 1
                        if 0 <= choice_num < len(options):
                            selected = choice_num
                            if selected == 0:
                                self.handle_add_task()
                            elif selected == 1:
                                self.handle_view_tasks()
                            elif selected == 2:
                                self.handle_update_task()
                            elif selected == 3:
                                self.handle_mark_complete()
                            elif selected == 4:
                                self.handle_delete_by_id()
                            elif selected == 5:
                                self.handle_set_priority()
                            elif selected == 6:
                                self.handle_set_due_date()
                            elif selected == 7:
                                self.handle_manage_tags()
                            elif selected == 8:
                                self.handle_search_tasks()
                            elif selected == 9:
                                self.handle_check_reminders()
                            elif selected == 10:  # Exit Application
                                print("\n👋 Thank you for using the Todo App! See you soon.\n")
                                break
                            else:
                                break
                        else:
                            print("Invalid choice. Please select a number between 1-10.")
                            input("Press Enter to continue...")
                    else:
                        print("Invalid input. Please enter a number or 'q'.")
                        input("Press Enter to continue...")
                except (EOFError, KeyboardInterrupt):
                    print("\n👋 Thank you for using the Todo App! See you soon.\n")
                    break

    # ==================== TASK OPERATIONS ====================

    def handle_add_task(self) -> None:
        """Handle adding a new task."""
        while True:
            self.clear_screen()
            self.print_header("ADD NEW TASK")
            print()
            self.print_info("Enter your task description below (max 200 chars).")
            print()

            self.console.print(" Task description (or leave empty to cancel): ", style="bold cyan", end="")
            title = sys.stdin.readline().strip()

            if not title:
                self.print_info("Cancelled.")
                self.press_enter_to_continue()
                return

            if len(title) > 200:
                self.print_error("Title is too long (max 200 characters).")
                self.press_enter_to_continue()
                continue

            task = self.tasklist.add(title)
            self.print_success(f"Your task '{title}' was added successfully!")
            print()

            self.console.print(" Add another task? (y/n): ", style="bold yellow", end="")
            # Use get_key() style single character read to be consistent
            ans = ""
            while ans not in ['y', 'n']:
                raw_ans = self.get_key().lower()
                if raw_ans == 'y':
                    ans = 'y'
                    print("y")
                elif raw_ans == 'n' or raw_ans == 'q':
                    ans = 'n'
                    print("n")

            if ans == 'n':
                break

    def handle_view_tasks(self) -> None:
        """Handle viewing tasks with navigation using screen buffer."""
        selected = 0
        while True:
            tasks = self.tasklist.get_all()
            if not tasks:
                self.draw_task_list(tasks)
                self.press_enter_to_continue()
                return

            try:
                with Live(console=self.console, auto_refresh=False, screen=True) as live:
                    while True:
                        selected = max(0, min(selected, len(tasks) - 1))

                        # Create the same static header appearance
                        from rich.console import Group
                        header_panel = Panel(Text("VIEW & MANAGE TASKS", style="bold cyan", justify="center"), box=ROUNDED, border_style="cyan", width=self.width)
                        display_group = Group(header_panel, Text("\n"), self.get_task_list_renderable(tasks, selected, mode="select"))

                        live.update(display_group, refresh=True)

                        key = self.get_key()
                        if key.lower() == 'q':
                            return
                        elif key == 'UP':
                            selected = max(0, selected - 1)
                        elif key == 'DOWN':
                            selected = min(len(tasks) - 1, selected + 1)
                        elif key in ['\r', '\n']:
                            live.stop()
                            self.show_task_actions(tasks[selected])
                            break # Refresh tasks state
            except Exception:
                # Fallback to regular display when screen buffer isn't available
                self.clear_screen()
                self.print_header("VIEW & MANAGE TASKS")
                print()

                # Display tasks in a simple format
                for i, task in enumerate(tasks):
                    status = "✅" if task.completed else "⏳"
                    priority_char = "H" if task.priority == Priority.HIGH else "M" if task.priority == Priority.MEDIUM else "L"
                    tags_str = f" #{','.join(task.tags[:2])}" if task.tags else ""
                    print(f"  {status} [{priority_char}] {task.id}. {task.title}{tags_str}")

                print(f"\nTotal tasks: {len(tasks)}")
                input("\nPress Enter to continue...")
                return

    def show_task_actions(self, task: Task) -> None:
        """Show task details and actions."""
        while True:
            self.clear_screen()
            status_style = "bold green" if task.completed else "bold yellow"
            status_text = "COMPLETED" if task.completed else "PENDING"

            detail_text = Text()
            detail_text.append(f"\n ID: {task.id}\n", style="dim")
            detail_text.append(f" STATUS: ", style="bold")
            detail_text.append(f"{status_text}\n", style=status_style)
            if hasattr(task, 'created_at') and task.created_at:
                detail_text.append(f" CREATED: {task.created_at.strftime('%Y-%m-%d %H:%M')}\n", style="dim")

            # Extended fields
            if hasattr(task, 'priority') and task.priority:
                priority_style = "bold red" if task.priority == Priority.HIGH else "yellow" if task.priority == Priority.MEDIUM else "green"
                detail_text.append(f" PRIORITY: ", style="bold")
                detail_text.append(f"{task.priority.value}\n", style=priority_style)

            if hasattr(task, 'tags') and task.tags:
                detail_text.append(f" TAGS: {', '.join(task.tags)}\n", style="cyan")

            if hasattr(task, 'due_date') and task.due_date:
                detail_text.append(f" DUE: {task.due_date.strftime('%Y-%m-%d %H:%M')}\n", style="bold yellow")

            if hasattr(task, 'recurrence') and task.recurrence and task.recurrence != Recurrence.NONE:
                detail_text.append(f" RECURRENCE: {task.recurrence.value}\n", style="magenta")

            detail_text.append("\n ────────────────────────────────────────\n", style="dim")
            detail_text.append(f"\n  {task.title}\n\n", style="bold white")
            detail_text.append(" ────────────────────────────────────────\n\n", style="dim")

            actions = [
                ("[c] Mark Complete", not task.completed),
                ("[d] Delete Task", True),
                ("[e] Edit Title", True),
                ("[q] Go Back", True)
            ]

            for label, active in actions:
                if active:
                    detail_text.append(f"  {label}\n")

            self.console.print(
                Panel(
                    detail_text,
                    title=f"TASK #{task.id}",
                    border_style="cyan",
                    width=self.width
                )
            )

            key = self.get_key().lower()
            if key == 'q':
                break
            elif key == 'c' and not task.completed:
                self.tasklist.toggle_complete(task.id)
                self.print_success(f"Task '{task.title}' marked as complete!")
                task = self.tasklist.get_by_id(task.id)
            elif key == 'd':
                if self.get_yes_no("Delete this task"):
                    task_title = task.title
                    self.tasklist.delete(task.id)
                    self.print_success(f"Task '{task_title}' deleted successfully.")
                    return
            elif key == 'e':
                self.handle_edit_task(task)
                task = self.tasklist.get_by_id(task.id)

    def handle_edit_task(self, task: Task) -> None:
        """Handle editing a task."""
        while True:
            self.clear_screen()
            self.print_header("EDIT TASK")
            print()
            self.print_info(f"Current title: {task.title}")
            print()
            self.console.print(" New title (max 200 chars): ", style="bold cyan", end="")
            new_title = sys.stdin.readline().strip()

            if not new_title:
                self.print_error("Update cancelled.")
                break

            if len(new_title) > 200:
                self.print_error("Title is too long (max 200 characters).")
                self.press_enter_to_continue()
                continue

            self.tasklist.update_title(task.id, new_title)
            self.print_success(f"Task '{new_title}' updated successfully.")
            break
        self.press_enter_to_continue()

    def handle_update_task(self) -> None:
        """Quick update from menu."""
        self.clear_screen()
        self.print_header("UPDATE TASK")
        print()
        self.console.print(" Enter Task ID to update: ", style="bold cyan", end="")
        try:
            val = sys.stdin.readline().strip()
            if not val: return
            task_id = int(val)
            task = self.tasklist.get_by_id(task_id)
            if task:
                self.handle_edit_task(task)
            else:
                self.print_error("Not found.")
                self.press_enter_to_continue()
        except ValueError:
            self.print_error("Invalid ID.")
            self.press_enter_to_continue()

    def handle_mark_complete(self) -> None:
        """Quick complete from menu."""
        self.clear_screen()
        self.print_header("MARK AS COMPLETE")
        print()
        self.console.print(" Enter Task ID: ", style="bold cyan", end="")
        try:
            val = sys.stdin.readline().strip()
            if not val: return
            task_id = int(val)
            task = self.tasklist.get_by_id(task_id)
            if task:
                task_title = task.title
                self.tasklist.toggle_complete(task_id)
                self.print_success(f"Task '{task_title}' marked as complete!")
            else:
                self.print_error("Not found.")
        except ValueError:
            self.print_error("Invalid ID.")
        self.press_enter_to_continue()

    def handle_delete_by_id(self) -> None:
        """Quick delete from menu."""
        self.clear_screen()
        self.print_header("DELETE BY ID")
        print()
        self.console.print(" Enter Task ID: ", style="bold cyan", end="")
        try:
            val = sys.stdin.readline().strip()
            if not val: return
            task_id = int(val)
            task = self.tasklist.get_by_id(task_id)
            if task:
                if self.get_yes_no(f"Delete task #{task_id}?"):
                    task_title = task.title
                    self.tasklist.delete(task_id)
                    self.print_success(f"Task '{task_title}' deleted successfully.")
            else:
                self.print_error("Not found.")
        except ValueError:
            self.print_error("Invalid ID.")
        self.press_enter_to_continue()

    def handle_set_priority(self) -> None:
        """Set task priority from menu."""
        self.clear_screen()
        self.print_header("SET TASK PRIORITY")
        print()
        self.console.print(" Enter Task ID: ", style="bold cyan", end="")
        try:
            val = sys.stdin.readline().strip()
            if not val: return
            task_id = int(val)
            task = self.tasklist.get_by_id(task_id)
            if not task:
                self.print_error("Not found.")
                self.press_enter_to_continue()
                return

            self.console.print(" Priority (High/Medium/Low): ", style="bold cyan", end="")
            priority_str = sys.stdin.readline().strip().capitalize()

            try:
                priority = Priority[priority_str.upper()]
                task = self.tasklist.update_priority(task_id, priority)
                if task:
                    self.print_success(f"Priority for '{task.title}' set to {priority.value}.")
                else:
                    self.print_error("Not found.")
            except KeyError:
                self.print_error(f"Invalid priority '{priority_str}'. Use High, Medium, or Low.")

        except ValueError:
            self.print_error("Invalid ID.")
        self.press_enter_to_continue()

    def handle_set_due_date(self) -> None:
        """Set task due date from menu."""
        self.clear_screen()
        self.print_header("SET TASK DUE DATE")
        print()
        self.console.print(" Enter Task ID: ", style="bold cyan", end="")
        try:
            val = sys.stdin.readline().strip()
            if not val: return
            task_id = int(val)
            task = self.tasklist.get_by_id(task_id)
            if not task:
                self.print_error("Not found.")
                self.press_enter_to_continue()
                return

            self.console.print(" Due date (YYYY-MM-DD or YYYY-MM-DD HH:MM): ", style="bold cyan", end="")
            due_date_str = sys.stdin.readline().strip()

            from datetime import datetime
            due_date = None

            # Try parsing with time (YYYY-MM-DD HH:MM)
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
            except ValueError:
                # Try parsing date only (YYYY-MM-DD)
                try:
                    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
                except ValueError:
                    self.print_error(f"Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM")
                    self.press_enter_to_continue()
                    return

            task = self.tasklist.set_due_date(task_id, due_date)
            if task:
                due_str = due_date.strftime("%Y-%m-%d %H:%M")
                self.print_success(f"Due date for '{task.title}' set to {due_str}.")
            else:
                self.print_error("Not found.")

        except ValueError:
            self.print_error("Invalid ID.")
        self.press_enter_to_continue()

    def handle_manage_tags(self) -> None:
        """Manage task tags from menu."""
        self.clear_screen()
        self.print_header("MANAGE TAGS")
        print()
        self.console.print(" Enter Task ID: ", style="bold cyan", end="")
        try:
            val = sys.stdin.readline().strip()
            if not val: return
            task_id = int(val)
            task = self.tasklist.get_by_id(task_id)
            if not task:
                self.print_error("Not found.")
                self.press_enter_to_continue()
                return

            self.console.print(f" Current tags: {', '.join(task.tags) if task.tags else 'None'}\n", style="dim")
            self.console.print(" Action (add/remove): ", style="bold cyan", end="")
            action = sys.stdin.readline().strip().lower()

            if action not in ["add", "remove"]:
                self.print_error("Invalid action. Use 'add' or 'remove'.")
                self.press_enter_to_continue()
                return

            self.console.print(" Tags (comma-separated): ", style="bold cyan", end="")
            tags_str = sys.stdin.readline().strip()
            tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]

            if not tags:
                self.print_error("No tags provided.")
                self.press_enter_to_continue()
                return

            if action == "add":
                task = self.tasklist.add_tags(task_id, tags)
                if task:
                    all_tags = ", ".join(task.tags)
                    self.print_success(f"Tags for '{task.title}' updated: {all_tags}.")
            else:
                task = self.tasklist.remove_tags(task_id, tags)
                if task:
                    remaining_tags = ", ".join(task.tags) if task.tags else "none"
                    self.print_success(f"Tags for '{task.title}' updated: {remaining_tags}.")

        except ValueError:
            self.print_error("Invalid ID.")
        self.press_enter_to_continue()

    def handle_search_tasks(self) -> None:
        """Search tasks by keyword."""
        self.clear_screen()
        self.print_header("SEARCH TASKS")
        print()
        self.console.print(" Enter keyword to search: ", style="bold cyan", end="")
        keyword = sys.stdin.readline().strip()

        if not keyword:
            self.print_info("Search cancelled.")
            self.press_enter_to_continue()
            return

        matching_tasks = self.tasklist.search(keyword)

        if not matching_tasks:
            self.print_info("No tasks match your search.")
        else:
            self.print_success(f"Here are the tasks matching your search:")
            print()
            for task in matching_tasks:
                status = "[x]" if task.completed else "[ ]"
                priority_char = task.priority.value[0] if task.priority else "M"
                tags_str = f" #{','.join(task.tags[:2])}" if task.tags else ""
                self.console.print(f"  {status} [{priority_char}] {task.id}. {task.title}{tags_str}")

        self.press_enter_to_continue()

    def handle_check_reminders(self) -> None:
        """Check for all tasks with due dates, including upcoming ones."""
        from .notifications import NotificationManager
        from datetime import datetime

        self.clear_screen()
        self.print_header("CHECK REMINDERS")
        print()

        current_time = datetime.now()

        # Get all tasks with due dates (both overdue and upcoming)
        all_tasks = self.tasklist.get_all()
        tasks_with_due_dates = [task for task in all_tasks if task.due_date is not None]

        # Separate overdue and upcoming tasks
        overdue_tasks = [task for task in tasks_with_due_dates if task.due_date < current_time]
        upcoming_tasks = [task for task in tasks_with_due_dates if task.due_date >= current_time and not task.completed]

        if not tasks_with_due_dates:
            self.print_info("No tasks with due dates.")
        else:
            if overdue_tasks:
                self.print_error(f"You have {len(overdue_tasks)} overdue task{'s' if len(overdue_tasks) > 1 else ''}:")
                for task in overdue_tasks:
                    due_str = task.due_date.strftime('%Y-%m-%d %H:%M')
                    self.console.print(f"  ⚠️  {task.title} (Due: {due_str})", style="bold red")

            if upcoming_tasks:
                self.print_success(f"You have {len(upcoming_tasks)} upcoming reminder{'s' if len(upcoming_tasks) > 1 else ''}:")
                for task in upcoming_tasks:
                    due_str = task.due_date.strftime('%Y-%m-%d %H:%M')
                    self.console.print(f"  📅 {task.title} (Due: {due_str})", style="bold yellow")

            if not overdue_tasks and not upcoming_tasks:
                self.print_info("No tasks with due dates.")

        self.press_enter_to_continue()
