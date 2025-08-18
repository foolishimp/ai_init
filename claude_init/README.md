# Claude Task Management System with BDD+TDD

A comprehensive methodology for AI-assisted software development using Claude Code (claude.ai/code) with integrated Behavior-Driven Development (BDD) and Test-Driven Development (TDD).

## 🚀 Quick Start

Install the Claude task management system in any project:

```bash
# Method 1: Download and run (Recommended - no git history)
curl -O https://raw.githubusercontent.com/foolishimp/claude_init/main/setup_claude_tasks.py
python setup_claude_tasks.py
rm setup_claude_tasks.py  # Optional: remove installer after use

# Method 2: One-liner pipe to Python
curl -sSL https://raw.githubusercontent.com/foolishimp/claude_init/main/setup_claude_tasks.py | python3

# Method 3: Install from GitHub repository
python setup_claude_tasks.py --source https://github.com/foolishimp/claude_init
```

## 📋 What This Provides

The Claude Task Management System with BDD+TDD establishes:

1. **Enhanced 9-Step BDD+TDD workflow** (SPECIFY → RED → GREEN → REFACTOR → VALIDATE)
2. **Behavior-Driven Development with Gherkin scenarios**
3. **AI-specific behavior patterns** (model validation, bias detection, compliance)
4. **Stakeholder collaboration through living documentation**
5. **Structured task tracking and documentation**
6. **Clear development principles**
7. **Pair programming patterns with AI**

## 🏗️ Structure Created

```
your-project/
├── CLAUDE.md                    # Project guidance for Claude
└── claude_tasks/
    ├── QUICK_REFERENCE.md       # Commands and BDD+TDD workflow
    ├── BDD_PROCESS.md           # Complete 9-step methodology
    ├── PRINCIPLES_QUICK_CARD.md # Core principles + BDD principles
    ├── DEVELOPMENT_PROCESS.md   # Legacy TDD methodology
    ├── TASK_TEMPLATE.md         # Template for tasks
    ├── behaviors/               # BDD specifications
    │   ├── features/            # Gherkin feature files
    │   ├── step_definitions/    # Test implementations
    │   ├── reports/             # Living documentation
    │   └── README.md           # BDD guidance
    ├── active/
    │   └── ACTIVE_TASKS.md      # Current tasks with behaviors
    └── finished/                # Completed tasks archive
```

## 🎯 Core Principles

1. **Test Driven Development** - Behaviors before tests before code
2. **Fail Fast & Root Cause** - Fix problems at source
3. **Modular & Maintainable** - Single responsibility
4. **Reuse Before Build** - Check existing code first
5. **Open Source First** - Suggest alternatives
6. **No Legacy Baggage** - Clean slate approach
7. **Perfectionist Excellence** - Best of breed only

### BDD Principles
- **Behavior-First**: Start with business outcomes
- **Stakeholder Collaboration**: Include business in specification
- **Living Documentation**: Scenarios become documentation
- **Outside-In Development**: Work from user value to implementation

## 💻 Usage

### Basic Installation

```bash
# In your project directory
python setup_claude_tasks.py
```

### From This Repository

```bash
python setup_claude_tasks.py --source https://github.com/foolishimp/claude_init
```

### From Local Clone

```bash
python setup_claude_tasks.py --source /path/to/claude_init --target ./myproject
```

### Options

- `--source PATH/URL` - Source for templates (default: embedded)
- `--target PATH` - Target directory (default: current)
- `--force` - Overwrite existing files
- `--no-git` - Skip .gitignore updates

## 🆕 Starting a Fresh Project

### Complete Setup Guide

1. **Create Your Project**
```bash
mkdir my-project && cd my-project
git init  # Optional but recommended
```

2. **Install Claude Task Management**
```bash
curl -O https://raw.githubusercontent.com/foolishimp/claude_init/main/setup_claude_tasks.py
python setup_claude_tasks.py
rm setup_claude_tasks.py
```

3. **Customize CLAUDE.md**
Edit the TODO sections with your project details:
- Repository overview
- Project structure
- Development commands
- Project-specific guidelines

4. **Create Your First Task**
Edit `claude_tasks/active/ACTIVE_TASKS.md`:
```markdown
### Task 1: Initialize Project
- **Priority**: High
- **Status**: Not Started
- **Description**: Set up project with testing
- **Acceptance Criteria**:
  - [ ] Tests configured
  - [ ] First test passing
  - [ ] Project structure defined
```

5. **Start with BDD+TDD**
```bash
# 1. SPECIFY: Write behavior scenario in Gherkin
touch claude_tasks/behaviors/features/my_feature.feature

# 2. RED: Write failing test from scenario
# 3. GREEN: Write code to pass
# 4. REFACTOR: Improve code quality
# 5. VALIDATE: Confirm behavior works
# Document in finished/ when complete
```

6. **Complete and Commit**
```bash
# Move task to finished/
mv task-notes claude_tasks/finished/$(date +%Y%m%d_%H%M)_task_name.md

# Commit with standard message
git add .
git commit -m "Task #1: Initialize project

Description of what was done.

Tests: X unit | Coverage: XX%
TDD: RED → GREEN → REFACTOR"
```

## 📚 Daily Workflow

1. **Start Session**: Review `claude_tasks/BDD_PROCESS.md`
2. **Check Tasks**: Read `claude_tasks/active/ACTIVE_TASKS.md`
3. **Follow BDD+TDD**: SPECIFY → RED → GREEN → REFACTOR → VALIDATE
4. **Document**: Move completed tasks to `finished/` with behavior validation
5. **Commit**: Use enhanced BDD+TDD message format

## 🤝 Working with Claude

When Claude Code works on your project, it will:

1. Check `CLAUDE.md` for project context
2. Follow BDD+TDD principles in `claude_tasks/`
3. Write Gherkin scenarios before coding
4. Use enhanced 9-step methodology
5. Track tasks with behavior specifications
6. Generate living documentation
7. Validate stakeholder expectations

## 📖 Documentation

### For Developers

- Review `QUICK_REFERENCE.md` for BDD+TDD commands
- Follow `BDD_PROCESS.md` for complete 9-step methodology
- Check `PRINCIPLES_QUICK_CARD.md` for standards and BDD principles
- Read `behaviors/README.md` for Gherkin scenario guidance

### For Claude

The system makes your project "Claude-aware" by:
- Providing enhanced BDD+TDD methodology
- Establishing stakeholder collaboration patterns
- Defining quality standards with behavior validation
- Creating comprehensive task tracking with scenarios
- Enabling living documentation generation

## 🔧 Customization

After installation:

1. Edit `CLAUDE.md` with project-specific details
2. Add initial tasks to `active/ACTIVE_TASKS.md`
3. Customize templates as needed
4. Commit changes to your repository

## 📦 Requirements

- Python 3.6+
- Git (for repository sources)
- Target project (any language)

## 📝 License

MIT License - Use freely in your projects

## 🙏 Contributing

Contributions welcome! The methodology is designed to be language-agnostic and universally applicable.

---

*Make your projects Claude-aware with structured, test-driven development.*