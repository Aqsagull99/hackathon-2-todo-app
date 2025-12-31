#!/usr/bin/env python3
"""Main entry point for the todo console application.

This module provides an interactive menu-based UI for managing todo tasks.
Run this file directly or via 'python -m todo_app.main'
"""
from .storage import TaskList
from .ui import InteractiveUI


def main() -> None:
    """Run the todo application."""
    tasklist = TaskList()
    ui = InteractiveUI(tasklist)
    ui.run()


if __name__ == "__main__":
    main()
