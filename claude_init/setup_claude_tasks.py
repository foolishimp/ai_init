#!/usr/bin/env python3
"""
Claude Task Management System Setup Script

This script installs the Claude task management system into any project,
making it "Claude-aware" with proper development methodology.

Usage:
    python setup_claude_tasks.py [options]
    
Options:
    --source PATH/URL   Source for claude_tasks (git repo, GitHub URL, or local path)
    --target PATH       Target directory for installation (default: current directory)
    --force            Overwrite existing files
    --no-git           Don't add .gitignore entries
"""

import os
import sys
import shutil
import argparse
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

# Embedded templates for when no source is provided
EMBEDDED_TEMPLATES = {
    "QUICK_REFERENCE.md": """# Task Management Quick Reference

## 🚀 Session Start Checklist
```bash
# 1. Check current state
git status
cat claude_tasks/active/ACTIVE_TASKS.md
npm test

# 2. Review core docs
cat claude_tasks/PRINCIPLES_QUICK_CARD.md
cat claude_tasks/DEVELOPMENT_PROCESS.md
```

## 🔴 Start a New Task (TDD Process)
1. **CHECK**: Current state and active tasks
2. **PLAN**: Update ACTIVE_TASKS.md to "In Progress"
3. **RED**: Write failing tests FIRST
4. **GREEN**: Write minimal code to pass tests
5. **REFACTOR**: Improve code quality

## ✅ Complete a Task
1. **DOCUMENT**: Create finished file
2. **COMMIT**: With descriptive message
3. **ARCHIVE**: Move to finished/
""",
    "PRINCIPLES_QUICK_CARD.md": """# Development Principles Quick Card

## The 7 Core Principles

1. **Test Driven Development** - No code without tests
2. **Fail Fast & Root Cause** - No workarounds, fix causes
3. **Modular & Maintainable** - Single responsibility
4. **Reuse Before Build** - Check existing code first
5. **Open Source First** - Suggest alternatives
6. **No Legacy Baggage** - Clean slate, no tech debt
7. **Perfectionist Excellence** - Best of breed only

## TDD Workflow
RED → GREEN → REFACTOR

## Code Quality Standards
- >80% test coverage
- Clear naming conventions
- Documented decisions
- No commented-out code
""",
    "ACTIVE_TASKS.md": """# Active Tasks

## Current Sprint
*Last Updated: [DATE]*

---

## Task Queue

### Task 1: [Example Task]
- **ID**: 1
- **Priority**: High/Medium/Low
- **Status**: Not Started
- **Estimated Time**: X hours
- **Dependencies**: None
- **Description**: [Clear description of what needs to be done]
- **Acceptance Criteria**:
  - [ ] Criterion 1
  - [ ] Criterion 2
  - [ ] Tests pass

---

## Completed Tasks
*Move to finished/ folder when complete*

## Notes
- Follow TDD: Write tests first
- Update status as you work
- Document in finished/ when complete
"""
}

class ClaudeTasksSetup:
    """Setup Claude task management system in a project."""
    
    def __init__(self, source: Optional[str] = None, target: str = ".", 
                 force: bool = False, no_git: bool = False):
        self.source = source
        # If no source specified, use the claude_tasks directory relative to this script
        if self.source is None:
            script_dir = Path(__file__).parent
            if (script_dir / "claude_tasks").exists():
                self.source = str(script_dir)
        
        self.target = Path(target).resolve()
        self.force = force
        self.no_git = no_git
        self.claude_tasks_dir = self.target / "claude_tasks"
        self.claude_md_path = self.target / "CLAUDE.md"
        
    def run(self):
        """Execute the setup process."""
        print("🚀 Claude Task Management System Setup")
        print(f"📁 Target directory: {self.target}")
        
        # Check what already exists
        claude_tasks_exists = self.claude_tasks_dir.exists()
        claude_md_exists = self.claude_md_path.exists()
        
        print(f"\n📋 Current state:")
        print(f"   claude_tasks/: {'✅ exists' if claude_tasks_exists else '❌ missing'}")
        print(f"   CLAUDE.md: {'✅ exists' if claude_md_exists else '❌ missing'}")
        
        # Install claude_tasks if missing or force flag is set
        if not claude_tasks_exists or self.force:
            if claude_tasks_exists and self.force:
                print(f"\n🔄 Reinstalling claude_tasks (--force flag)")
            else:
                print(f"\n📦 Installing claude_tasks...")
            
            # Create claude_tasks directory
            self._create_directory_structure()
            
            # Copy or create files
            if self.source:
                self._copy_from_source()
            else:
                self._create_from_templates()
        else:
            print(f"\n⏭️  Skipping claude_tasks (already exists)")
        
        # Handle CLAUDE.md if missing or force flag is set
        if not claude_md_exists or self.force:
            if claude_md_exists and self.force:
                print(f"\n🔄 Updating CLAUDE.md (--force flag)")
            else:
                print(f"\n📝 Creating CLAUDE.md...")
            self._handle_claude_md()
        else:
            print(f"\n⏭️  Skipping CLAUDE.md (already exists)")
        
        
        # Add .gitignore entries
        if not self.no_git:
            self._update_gitignore()
        
        print("\n✅ Setup complete!")
        self._print_next_steps()
    
    def _create_directory_structure(self):
        """Create the claude_tasks directory structure."""
        directories = [
            self.claude_tasks_dir,
            self.claude_tasks_dir / "active",
            self.claude_tasks_dir / "finished", 
            self.claude_tasks_dir / "todo",
            self.target / ".claude",
            self.target / ".claude" / "commands",
        ]
        
        for directory in directories:
            if not directory.exists():
                directory.mkdir(parents=True, exist_ok=True)
                print(f"📁 Created: {directory.relative_to(self.target)}")
    
    def _copy_from_source(self):
        """Copy files from source repository or directory."""
        temp_dir = None
        
        try:
            # Determine source type and get path
            if self.source.startswith(("http://", "https://", "git@")):
                # Clone from git
                temp_dir = tempfile.mkdtemp()
                print(f"📥 Cloning from: {self.source}")
                subprocess.run(
                    ["git", "clone", "--depth", "1", self.source, temp_dir],
                    check=True,
                    capture_output=True
                )
                # Remove .git folder to avoid confusion
                git_dir = Path(temp_dir) / ".git"
                if git_dir.exists():
                    shutil.rmtree(git_dir)
                source_path = Path(temp_dir) / "claude_tasks"
            else:
                # Local path
                source_path = Path(self.source)
                if not source_path.exists():
                    raise FileNotFoundError(f"Source not found: {source_path}")
                
                # Check if source has claude_tasks subdirectory
                if (source_path / "claude_tasks").exists():
                    source_path = source_path / "claude_tasks"
            
            # Copy files
            self._copy_files(source_path)
            
        finally:
            # Clean up temp directory
            if temp_dir and Path(temp_dir).exists():
                shutil.rmtree(temp_dir)
    
    def _copy_files(self, source_path: Path):
        """Copy files from source to target."""
        if not source_path.exists():
            print(f"⚠️  Source claude_tasks not found, using embedded templates")
            self._create_from_templates()
            return
        
        # Files to copy
        files_to_copy = [
            "QUICK_REFERENCE.md",
            "PRINCIPLES_QUICK_CARD.md",
            "DEVELOPMENT_PROCESS.md",
            "PAIR_PROGRAMMING_WITH_CLAUDE.md",
            "UNIFIED_PRINCIPLES.md",
            "SESSION_STARTER.md",
            "TASK_TEMPLATE.md",
        ]
        
        for file_name in files_to_copy:
            source_file = source_path / file_name
            target_file = self.claude_tasks_dir / file_name
            
            if source_file.exists():
                if target_file.exists() and not self.force:
                    print(f"⏭️  Skipping existing: {file_name}")
                else:
                    shutil.copy2(source_file, target_file)
                    print(f"📄 Copied: {file_name}")
        
        # Copy active tasks if exists
        active_tasks = source_path / "active" / "ACTIVE_TASKS.md"
        if active_tasks.exists():
            target_active = self.claude_tasks_dir / "active" / "ACTIVE_TASKS.md"
            if not target_active.exists() or self.force:
                shutil.copy2(active_tasks, target_active)
                print(f"📄 Copied: active/ACTIVE_TASKS.md")
        
        # Copy todo files if they exist
        todo_list = source_path / "todo" / "TODO_LIST.md"
        if todo_list.exists():
            target_todo = self.claude_tasks_dir / "todo" / "TODO_LIST.md"
            if not target_todo.exists() or self.force:
                shutil.copy2(todo_list, target_todo)
                print(f"📄 Copied: todo/TODO_LIST.md")
        
        todo_command = source_path / "todo" / "todo.md"
        if todo_command.exists():
            target_todo_cmd = self.claude_tasks_dir / "todo" / "todo.md"
            if not target_todo_cmd.exists() or self.force:
                shutil.copy2(todo_command, target_todo_cmd)
                print(f"📄 Copied: todo/todo.md")
        
        # Copy .claude commands if they exist
        claude_commands_source = source_path.parent / ".claude" / "commands"
        if claude_commands_source.exists():
            claude_commands_target = self.target / ".claude" / "commands"
            for cmd_file in claude_commands_source.glob("*.md"):
                target_cmd = claude_commands_target / cmd_file.name
                if not target_cmd.exists() or self.force:
                    shutil.copy2(cmd_file, target_cmd)
                    print(f"📄 Copied: .claude/commands/{cmd_file.name}")
    
    def _create_from_templates(self):
        """Create files from embedded templates."""
        print("📝 Creating from embedded templates...")
        
        for file_name, content in EMBEDDED_TEMPLATES.items():
            if file_name == "ACTIVE_TASKS.md":
                target_file = self.claude_tasks_dir / "active" / file_name
            else:
                target_file = self.claude_tasks_dir / file_name
            
            if target_file.exists() and not self.force:
                print(f"⏭️  Skipping existing: {file_name}")
            else:
                # Update date in content
                content = content.replace("[DATE]", datetime.now().strftime("%Y-%m-%d"))
                target_file.write_text(content)
                print(f"📄 Created: {file_name}")
        
        # Create todo files and commands
        self._create_todo_files()
        self._create_claude_commands()
    
    def _create_todo_files(self):
        """Create todo-specific files."""
        # Create TODO_LIST.md
        todo_list_content = """# Todo List

## Quick Todos
*Items added via /todo command - convert to formal tasks when ready*

*Last Updated: [DATE]*

---

## Todo Items

*No todos currently. Use /todo "description" to add items quickly.*

---

## Instructions

### Adding Todos
- Use the `/todo` slash command: `/todo "implement new feature"`
- Items are added with timestamp for quick capture
- Convert important items to formal tasks in active/ACTIVE_TASKS.md

### Managing Todos
- ✅ **Completed**: Mark with checkmark and move to finished tasks if significant
- ❌ **Cancelled**: Remove or mark as cancelled if no longer needed
- ➡️ **Promoted**: Move to active/ACTIVE_TASKS.md as formal tasks

### Todo vs Task Difference
- **Todos**: Quick capture, informal, immediate thoughts
- **Tasks**: Formal, estimated time, acceptance criteria, TDD process

### Cleanup Process
- Review todos regularly (daily/weekly)
- Promote important items to formal tasks
- Remove completed or outdated items
- Keep this list focused and actionable

---

*Todo items are meant for quick capture. For formal development work, create proper tasks in active/ACTIVE_TASKS.md following the TDD methodology.*
"""
        
        todo_list_file = self.claude_tasks_dir / "todo" / "TODO_LIST.md"
        if not todo_list_file.exists() or self.force:
            content = todo_list_content.replace("[DATE]", datetime.now().strftime("%Y-%m-%d"))
            todo_list_file.write_text(content)
            print(f"📄 Created: todo/TODO_LIST.md")
        
        # Create /todo command
        todo_command_content = """# Add Todo Item

Add the following item to the todo list:

**Todo Item**: {todo_text}

## Instructions:

1. **Read current todo list** from `claude_tasks/todo/TODO_LIST.md`

2. **Add new todo item** in the "Todo Items" section using this format:
   ```markdown
   ### {current_timestamp} - 📝 New
   **Todo**: {todo_description}
   **Added**: {current_date_time}
   
   ---
   ```

3. **Update timestamp** in the "Last Updated" field at the top

4. **Keep organized** - add new items at the top of the Todo Items section

5. **Brief confirmation** - Simply confirm "Added to todo list" without repeating the item

This provides quick capture of ideas and tasks during development. Items can later be promoted to formal tasks in `claude_tasks/active/ACTIVE_TASKS.md` when ready for TDD development work.

**Usage Examples:**
- `/todo "add error handling to login"`
- `/todo "investigate performance issue"`
- `/todo "refactor user service"`
"""
        
        todo_command_file = self.target / ".claude" / "commands" / "todo.md"
        if not todo_command_file.exists() or self.force:
            todo_command_file.write_text(todo_command_content)
            print(f"📄 Created: .claude/commands/todo.md")
    
    def _create_claude_commands(self):
        """Create Claude slash commands."""
        commands_dir = self.target / ".claude" / "commands"
        
        # Create /refresh command
        refresh_content = """# Refresh Development Context

Please perform the following tasks in order:

1. **Reread Core Documentation:**
   - Read CLAUDE.md to understand project context and development methodology
   - Read claude_tasks/QUICK_REFERENCE.md for TDD workflow
   - Read claude_tasks/PRINCIPLES_QUICK_CARD.md for the 7 core principles
   - Read claude_tasks/DEVELOPMENT_PROCESS.md for complete methodology

2. **Review Active Tasks:**
   - Read claude_tasks/active/ACTIVE_TASKS.md
   - Analyze current task statuses and priorities
   - Identify any tasks marked as "completed" or "done"

3. **Review Todo List:**
   - Read claude_tasks/todo/TODO_LIST.md
   - Check for any todos that should be promoted to formal tasks
   - Note any completed todos that can be removed

4. **Clean Up Completed Tasks:**
   - For any completed tasks found in ACTIVE_TASKS.md:
     - Create properly formatted files in claude_tasks/finished/ using format YYYYMMDD_HHMM_task_name.md
     - Use the task template format from QUICK_REFERENCE.md
     - Include test coverage, TDD process notes, and results
     - Remove the completed tasks from ACTIVE_TASKS.md
   - Update the "Last Updated" timestamp in ACTIVE_TASKS.md

5. **Provide Summary:**
   - Summarize current project state
   - List remaining active tasks with priorities
   - List current todos and suggest promotions
   - Note any blockers or issues found
   - Suggest next steps based on current task queue

This command ensures I have full context of the project's development methodology and current state before proceeding with any work.
"""
        
        refresh_file = commands_dir / "refresh.md"
        if not refresh_file.exists() or self.force:
            refresh_file.write_text(refresh_content)
            print(f"📄 Created: .claude/commands/refresh.md")
        else:
            print(f"⏭️  Skipping existing: .claude/commands/refresh.md")
        
        # Create /todo command  
        todo_content = """# Add Todo Item

Add the following item to the todo list:

**Todo Item**: {todo_text}

## Instructions:

1. **Read current todo list** from `claude_tasks/todo/TODO_LIST.md`

2. **Add new todo item** in the "Todo Items" section using this format:
   ```markdown
   ### {current_timestamp} - 📝 New
   **Todo**: {todo_description}
   **Added**: {current_date_time}
   
   ---
   ```

3. **Update timestamp** in the "Last Updated" field at the top

4. **Keep organized** - add new items at the top of the Todo Items section

5. **Brief confirmation** - Simply confirm "Added to todo list" without repeating the item

This provides quick capture of ideas and tasks during development. Items can later be promoted to formal tasks in `claude_tasks/active/ACTIVE_TASKS.md` when ready for TDD development work.

**Usage Examples:**
- `/todo "add error handling to login"`
- `/todo "investigate performance issue"`
- `/todo "refactor user service"`
"""
        
        todo_file = commands_dir / "todo.md"
        if not todo_file.exists() or self.force:
            todo_file.write_text(todo_content)
            print(f"📄 Created: .claude/commands/todo.md")
        else:
            print(f"⏭️  Skipping existing: .claude/commands/todo.md")
    
    def _handle_claude_md(self):
        """Create or update CLAUDE.md file."""
        if self.claude_md_path.exists():
            self._update_existing_claude_md()
        else:
            self._create_new_claude_md()
    
    def _update_existing_claude_md(self):
        """Prepend task system reference to existing CLAUDE.md."""
        print(f"📝 Updating existing CLAUDE.md...")
        
        existing_content = self.claude_md_path.read_text()
        
        # Check if already has task system reference
        if "claude_tasks" in existing_content:
            print("✓ CLAUDE.md already references task system")
            return
        
        # Prepend reference section
        reference_section = """# CLAUDE.md

## 📋 Claude Development Process
This project now uses the Claude Task Management System for AI-assisted development.

### Key Documents
- `claude_tasks/QUICK_REFERENCE.md` - Quick commands and workflow
- `claude_tasks/DEVELOPMENT_PROCESS.md` - Full TDD methodology
- `claude_tasks/PRINCIPLES_QUICK_CARD.md` - Core development principles
- `claude_tasks/active/ACTIVE_TASKS.md` - Current task tracking

---

""" 
        
        # Remove existing header if present
        if existing_content.startswith("# CLAUDE.md"):
            existing_content = existing_content[existing_content.find("\n")+1:]
        
        new_content = reference_section + existing_content
        
        if not self.force:
            # Backup existing file
            backup_path = self.claude_md_path.with_suffix(".md.backup")
            shutil.copy2(self.claude_md_path, backup_path)
            print(f"📋 Backed up to: {backup_path.name}")
        
        self.claude_md_path.write_text(new_content)
        print("✅ Updated CLAUDE.md with task system reference")
    
    def _create_new_claude_md(self):
        """Create new CLAUDE.md from template."""
        print("📝 Creating new CLAUDE.md...")
        
        # Get template from source if available
        template_path = None
        if self.source:
            if self.source.startswith(("http://", "https://", "git@")):
                # Would need to clone again, skip for now
                pass
            else:
                source_path = Path(self.source)
                if (source_path / "CLAUDE.md").exists():
                    template_path = source_path / "CLAUDE.md"
        
        if template_path and template_path.exists():
            shutil.copy2(template_path, self.claude_md_path)
        else:
            # Use embedded template
            content = self._get_claude_md_template()
            self.claude_md_path.write_text(content)
        
        print("✅ Created CLAUDE.md")
    
    def _get_claude_md_template(self) -> str:
        """Get the CLAUDE.md template."""
        return """# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Claude Development Process

This project follows the Claude Task Management System. See `claude_tasks/` for:
- `QUICK_REFERENCE.md` - Quick commands and TDD workflow
- `DEVELOPMENT_PROCESS.md` - Complete methodology
- `PRINCIPLES_QUICK_CARD.md` - Core principles
- `active/ACTIVE_TASKS.md` - Current tasks

## Repository Overview

[TODO: Add project description]

## Project Structure

```
[TODO: Document structure]
```

## Common Development Commands

### Testing
```bash
# Run tests
npm test  # or appropriate command

# With coverage
npm test -- --coverage

# Watch mode
npm test -- --watch
```

## Working with this Codebase

Follow TDD: RED → GREEN → REFACTOR

See `claude_tasks/` for detailed methodology.
"""
    

    def _update_gitignore(self):
        """Add appropriate .gitignore entries."""
        gitignore_path = self.target / ".gitignore"
        
        entries_to_add = [
            "\n# Claude task management",
            "*.backup",
            "CLAUDE.md.backup",
        ]
        
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            
            # Check if already has claude entries
            if "claude_tasks" in content:
                print("✓ .gitignore already configured")
                return
            
            # Append entries
            if not content.endswith("\n"):
                content += "\n"
            
            content += "\n".join(entries_to_add) + "\n"
            gitignore_path.write_text(content)
            print("📝 Updated .gitignore")
        else:
            # Create new .gitignore
            content = "\n".join(entries_to_add) + "\n"
            gitignore_path.write_text(content)
            print("📝 Created .gitignore")
    
    def _print_next_steps(self):
        """Print next steps for the user."""
        claude_tasks_exists = self.claude_tasks_dir.exists()
        claude_md_exists = self.claude_md_path.exists()
        
        print("\n📚 Next Steps:")
        
        step_num = 1
        
        if claude_tasks_exists:
            print(f"{step_num}. Review claude_tasks/QUICK_REFERENCE.md for workflow")
            step_num += 1
            print(f"{step_num}. Read claude_tasks/PRINCIPLES_QUICK_CARD.md for principles")
            step_num += 1
            print(f"{step_num}. Add your first task to claude_tasks/active/ACTIVE_TASKS.md")
            step_num += 1
        
        if claude_md_exists:
            print(f"{step_num}. Customize CLAUDE.md with project-specific information")
            step_num += 1
        
        # Only suggest git commit if something was actually installed
        if claude_tasks_exists or claude_md_exists:
            print(f"{step_num}. Commit the changes: git add . && git commit -m 'Add Claude task management system'")
            step_num += 1
        
        if claude_tasks_exists:
            print("\n🎯 Start coding with: cat claude_tasks/SESSION_STARTER.md")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Setup Claude Task Management System in your project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use embedded templates in current directory
  python setup_claude_tasks.py
  
  # From GitHub repository
  python setup_claude_tasks.py --source https://github.com/user/claude_init
  
  # From local directory
  python setup_claude_tasks.py --source /path/to/claude_tasks --target ./myproject
  
  # Force overwrite existing files
  python setup_claude_tasks.py --force
        """
    )
    
    parser.add_argument(
        "--source",
        help="Source for claude_tasks (git repo URL or local path)",
        default=None
    )
    
    parser.add_argument(
        "--target",
        help="Target directory for installation (default: current directory)",
        default="."
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files"
    )
    
    parser.add_argument(
        "--no-git",
        action="store_true",
        help="Don't add .gitignore entries"
    )
    
    args = parser.parse_args()
    
    # Run setup
    setup = ClaudeTasksSetup(
        source=args.source,
        target=args.target,
        force=args.force,
        no_git=args.no_git
    )
    
    try:
        setup.run()
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()