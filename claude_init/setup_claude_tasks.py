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
cat claude_tasks/BDD_PROCESS.md
```

## 🔴 Start a New Task (BDD+TDD Process)
1. **CHECK**: Current state and active tasks
2. **SPECIFY**: Write behavior in Gherkin (behaviors/features/)
3. **PLAN**: Update ACTIVE_TASKS.md with behaviors
4. **RED**: Write failing tests from specifications
5. **GREEN**: Write minimal code to pass tests
6. **REFACTOR**: Improve code quality
7. **VALIDATE**: Confirm behaviors work as specified
8. **DOCUMENT**: Record behaviors + implementation
9. **COMMIT**: Save with BDD+TDD message

## ✅ Complete a Task
1. **VALIDATE**: All scenarios pass
2. **DOCUMENT**: Create finished file with behaviors
3. **COMMIT**: With BDD+TDD message format
4. **ARCHIVE**: Move to finished/

## 🥒 BDD Quick Commands
```bash
# Create new feature file
touch claude_tasks/behaviors/features/my_feature.feature

# Run behavior tests (example with Cucumber)
npx cucumber-js claude_tasks/behaviors/features/

# Generate living documentation
npx cucumber-js --format html > claude_tasks/behaviors/reports/living_docs.html
```

## 📝 Gherkin Template
```gherkin
Feature: [Feature Name]
  As a [user type]
  I want to [goal]
  So that [business value]

  Scenario: [Scenario Name]
    Given [context]
    When [action]
    Then [outcome]
    And [additional outcome]
```
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

## BDD+TDD Workflow
SPECIFY → RED → GREEN → REFACTOR → VALIDATE

## Code Quality Standards
- >80% test coverage
- All behaviors validated
- Clear naming conventions
- Living documentation current
- No commented-out code

## BDD Principles
- **Behavior-First**: Start with business outcomes
- **Stakeholder Collaboration**: Include business in specification
- **Living Documentation**: Scenarios become documentation
- **Outside-In Development**: Work from user value to implementation
- **Ubiquitous Language**: Shared vocabulary across team
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
- **Feature File**: `behaviors/features/example.feature` (if applicable)
- **Behaviors to Implement**:
  - [ ] Scenario: [Business scenario description]
  - [ ] Scenario: [Another scenario if applicable]
- **Acceptance Criteria**:
  - [ ] All scenarios in feature file pass
  - [ ] Unit tests pass with >80% coverage
  - [ ] Integration tests validate behavior
  - [ ] Stakeholder approval on behavior validation

---

## Completed Tasks
*Move to finished/ folder when complete*

## Notes
- Follow BDD+TDD: SPECIFY → RED → GREEN → REFACTOR → VALIDATE
- Write Gherkin scenarios before coding
- Update status as you work
- Document behaviors and implementation in finished/
- Include stakeholders in behavior validation
""",
    "BDD_PROCESS.md": """# BDD+TDD Development Process

## Enhanced 9-Step Process

### 1. CHECK → Current state and active tasks
- Review `claude_tasks/active/ACTIVE_TASKS.md`
- Check git status and test state
- Understand current project context

### 2. SPECIFY → Write behavior specifications in Gherkin
- Create or update feature files in `behaviors/features/`
- Use Given/When/Then format
- Focus on business value and user outcomes
- Include AI-specific scenarios (accuracy, bias, compliance)

### 3. PLAN → Update ACTIVE_TASKS.md with behaviors
- Link behaviors to feature files
- Define acceptance criteria
- Estimate effort and dependencies

### 4. RED → Write failing tests from specifications
- Create unit tests based on Gherkin scenarios
- Write integration tests for behavior validation
- Ensure tests fail initially

### 5. GREEN → Write minimal code to pass tests
- Implement just enough code to make tests pass
- Focus on making behaviors work
- Don't optimize yet

### 6. REFACTOR → Improve code quality
- Clean up implementation while keeping tests green
- Extract reusable components
- Improve naming and structure

### 7. VALIDATE → Confirm behaviors work as specified
- Run all scenarios in feature files
- Verify acceptance criteria are met
- Test with real data if applicable
- Confirm stakeholder expectations

### 8. DOCUMENT → Record implementation and behaviors
- Update living documentation
- Document design decisions
- Record behavior validation results
- Create finished task documentation

### 9. COMMIT → Save with BDD+TDD message
- Include both behavior and technical details
- Reference feature files and test coverage
- Follow commit message template

## BDD Benefits for AI Projects

### Stakeholder Alignment
- Business-readable specifications in Gherkin
- Clear acceptance criteria before implementation
- Living documentation that stays current
- Collaborative requirement definition

### AI-Specific Behaviors
- Model accuracy requirements as testable scenarios
- Bias detection and mitigation workflows
- Human-in-loop validation processes
- Regulatory compliance behaviors
- Data quality and validation scenarios

### Example AI Project Behaviors

```gherkin
Feature: AI Model Accuracy Validation
  As a data scientist
  I want to validate model accuracy automatically
  So that I can ensure reliable AI recommendations

  Scenario: High-stakes prediction validation
    Given a trained AI model for financial predictions
    And a prediction with confidence score below 85%
    When the system processes the prediction
    Then it should flag for human review
    And it should log the uncertainty for audit
    And it should not execute automated actions

  Scenario: Bias detection in recommendations
    Given an AI recommendation system
    And a set of test cases covering protected groups
    When the system generates recommendations
    Then it should show consistent accuracy across groups
    And it should flag any significant bias detected
    And it should provide explanation for flagged cases
```

## Commit Message Template

```
Task #X: [Brief description]

BEHAVIOR: [Business value delivered]
- Feature: [Gherkin scenarios that now pass]
- Stakeholder impact: [Who benefits and how]

TECHNICAL: [Implementation details]
- TDD: [Tests written/passing] | Coverage: [X%]
- Architecture: [Key design decisions]
- Integration: [Systems affected]

🤖 Generated with [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

## Tool Integration

### Recommended BDD Tools
- **Cucumber.js** (JavaScript) or **behave** (Python)
- **Allure** or **Cucumber Reports** for living documentation
- **VS Code Cucumber Extension** for Gherkin editing
- **Gherkin syntax highlighting** in IDE

### File Organization
```
behaviors/
├── features/           # Gherkin feature files
│   ├── user_stories.feature
│   ├── ai_validation.feature
│   └── compliance.feature
├── step_definitions/   # Test implementations
│   ├── common_steps.js
│   └── ai_steps.js
└── reports/           # Generated documentation
    ├── cucumber_report.html
    └── living_docs.md
```

## Best Practices

1. **Start with behaviors** before writing any code
2. **Write scenarios collaboratively** with stakeholders
3. **Keep scenarios focused** on business outcomes
4. **Use consistent language** across features
5. **Validate behaviors regularly** with stakeholders
6. **Maintain living documentation** automatically
7. **Include AI-specific scenarios** for model validation
8. **Test edge cases** and error conditions
9. **Document assumptions** and constraints
10. **Review and refine** scenarios based on feedback
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
            self.claude_tasks_dir / "behaviors",
            self.claude_tasks_dir / "behaviors" / "features",
            self.claude_tasks_dir / "behaviors" / "step_definitions",
            self.claude_tasks_dir / "behaviors" / "reports",
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
            "BDD_PROCESS.md",
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
        
        # Copy behaviors directory if it exists
        behaviors_source = source_path / "behaviors"
        if behaviors_source.exists():
            behaviors_target = self.claude_tasks_dir / "behaviors"
            
            # Copy behaviors README
            readme_source = behaviors_source / "README.md"
            if readme_source.exists():
                readme_target = behaviors_target / "README.md"
                if not readme_target.exists() or self.force:
                    shutil.copy2(readme_source, readme_target)
                    print(f"📄 Copied: behaviors/README.md")
            
            # Copy features directory
            features_source = behaviors_source / "features"
            if features_source.exists():
                features_target = behaviors_target / "features"
                for feature_file in features_source.glob("*.feature"):
                    target_feature = features_target / feature_file.name
                    if not target_feature.exists() or self.force:
                        shutil.copy2(feature_file, target_feature)
                        print(f"📄 Copied: behaviors/features/{feature_file.name}")
            
            # Copy step_definitions directory
            steps_source = behaviors_source / "step_definitions"
            if steps_source.exists():
                steps_target = behaviors_target / "step_definitions"
                for step_file in steps_source.glob("*.js"):
                    target_step = steps_target / step_file.name
                    if not target_step.exists() or self.force:
                        shutil.copy2(step_file, target_step)
                        print(f"📄 Copied: behaviors/step_definitions/{step_file.name}")
    
    def _create_from_templates(self):
        """Create files from embedded templates."""
        print("📝 Creating from embedded templates...")
        
        for file_name, content in EMBEDDED_TEMPLATES.items():
            if file_name == "ACTIVE_TASKS.md":
                target_file = self.claude_tasks_dir / "active" / file_name
            elif file_name == "BDD_PROCESS.md":
                target_file = self.claude_tasks_dir / file_name
            else:
                target_file = self.claude_tasks_dir / file_name
            
            if target_file.exists() and not self.force:
                print(f"⏭️  Skipping existing: {file_name}")
            else:
                # Update date in content
                content = content.replace("[DATE]", datetime.now().strftime("%Y-%m-%d"))
                target_file.write_text(content)
                print(f"📄 Created: {file_name}")
        
        # Create todo files, BDD files, and commands
        self._create_todo_files()
        self._create_bdd_files()
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
    
    def _create_bdd_files(self):
        """Create BDD-specific template files."""
        
        # Create example feature file
        example_feature_content = """Feature: Example AI Project Behavior
  As a [stakeholder type]
  I want to [achieve some goal]
  So that [business value is delivered]

  Background:
    Given the system is properly configured
    And all dependencies are available

  Scenario: Successful feature operation
    Given [initial context or state]
    When [action is performed]
    Then [expected outcome occurs]
    And [additional verification]

  Scenario: Error handling
    Given [error conditions exist]
    When [action is attempted]
    Then [appropriate error handling occurs]
    And [system remains stable]

  # AI-Specific Scenario Examples
  Scenario: Model accuracy validation
    Given a trained AI model
    And a test dataset with known correct answers
    When the model makes predictions
    Then the accuracy should be above the minimum threshold
    And confidence scores should be properly calibrated

  Scenario: Bias detection and mitigation
    Given an AI recommendation system
    And test cases representing different demographic groups
    When recommendations are generated
    Then the system should show consistent performance across groups
    And any detected bias should be flagged for review
"""
        
        example_feature_file = self.claude_tasks_dir / "behaviors" / "features" / "example.feature"
        if not example_feature_file.exists() or self.force:
            example_feature_file.write_text(example_feature_content)
            print(f"📄 Created: behaviors/features/example.feature")
        
        # Create step definitions template
        step_definitions_content = """// Step Definitions Template
// This file shows examples of how to implement Gherkin steps

// Example step definitions for Cucumber.js
// Adapt these patterns to your testing framework

const { Given, When, Then } = require('@cucumber/cucumber');
const assert = require('assert');

// Context steps
Given('the system is properly configured', function () {
  // Setup system configuration
  this.systemConfig = {
    initialized: true,
    dependencies: 'available'
  };
});

Given('all dependencies are available', function () {
  // Verify dependencies
  assert(this.systemConfig.dependencies === 'available');
});

// Action steps
When('I perform {string}', function (action) {
  // Perform the specified action
  this.lastAction = action;
  this.result = performAction(action);
});

// Outcome verification steps
Then('the result should be {string}', function (expectedResult) {
  assert.strictEqual(this.result, expectedResult);
});

Then('the system should remain stable', function () {
  // Verify system stability
  assert(this.systemConfig.initialized === true);
});

// AI-specific step definitions
Given('a trained AI model', function () {
  this.model = {
    trained: true,
    accuracy: 0.95,
    lastUpdated: new Date()
  };
});

When('the model makes predictions on {string}', function (dataset) {
  this.predictions = this.model.predict(dataset);
});

Then('the accuracy should be above {float}', function (threshold) {
  assert(this.predictions.accuracy > threshold);
});

Then('confidence scores should be properly calibrated', function () {
  assert(this.predictions.confidence >= 0 && this.predictions.confidence <= 1);
});

// Helper functions (implement based on your system)
function performAction(action) {
  // Implement action logic
  return `Result of ${action}`;
}
"""
        
        step_definitions_file = self.claude_tasks_dir / "behaviors" / "step_definitions" / "common_steps.js"
        if not step_definitions_file.exists() or self.force:
            step_definitions_file.write_text(step_definitions_content)
            print(f"📄 Created: behaviors/step_definitions/common_steps.js")
        
        # Create BDD configuration template
        cucumber_config_content = """// Cucumber.js Configuration
// cucumber.js

module.exports = {
  default: {
    require: [
      'claude_tasks/behaviors/step_definitions/**/*.js'
    ],
    format: [
      'progress-bar',
      'html:claude_tasks/behaviors/reports/cucumber_report.html',
      'json:claude_tasks/behaviors/reports/cucumber_report.json'
    ],
    paths: [
      'claude_tasks/behaviors/features/**/*.feature'
    ],
    parallel: 2
  }
};
"""
        
        cucumber_config_file = self.target / "cucumber.js"
        if not cucumber_config_file.exists() or self.force:
            cucumber_config_file.write_text(cucumber_config_content)
            print(f"📄 Created: cucumber.js")
        
        # Create README for behaviors directory
        behaviors_readme_content = """# Behaviors Directory

This directory contains Behavior-Driven Development (BDD) specifications and tests.

## Structure

### features/
Contains Gherkin feature files that describe business behaviors in natural language.
- Write scenarios from the user's perspective
- Focus on business value and outcomes
- Use consistent language across features
- Include AI-specific scenarios (accuracy, bias, compliance)

### step_definitions/
Contains the implementation of Gherkin steps.
- Map Gherkin steps to actual code
- Keep step definitions reusable
- Organize by domain or feature area
- Include setup and teardown logic

### reports/
Generated documentation and test reports.
- Cucumber HTML reports
- Living documentation
- Test coverage reports
- Stakeholder-friendly summaries

## Writing Good BDD Scenarios

### Template
```gherkin
Feature: [Feature Name]
  As a [user type]
  I want to [goal]
  So that [business value]

  Scenario: [Scenario Name]
    Given [context]
    When [action]
    Then [outcome]
```

### AI Project Examples

#### Model Validation
```gherkin
Scenario: High-confidence predictions are accepted
  Given a trained sentiment analysis model
  And a text input with clear sentiment
  When the model analyzes the text
  Then the confidence score should be above 90%
  And the prediction should be automatically accepted
```

#### Human-in-Loop Validation
```gherkin
Scenario: Low-confidence predictions require human review
  Given a trained classification model
  And an ambiguous input case
  When the model makes a prediction
  Then the confidence score should be below 80%
  And the prediction should be flagged for human review
  And the case should be queued for expert validation
```

#### Bias Detection
```gherkin
Scenario: Fair treatment across demographic groups
  Given a recommendation system
  And test cases representing different demographic groups
  When recommendations are generated for each group
  Then the approval rates should be within 5% across groups
  And any statistical bias should be flagged for investigation
```

## Running BDD Tests

```bash
# Install Cucumber.js
npm install --save-dev @cucumber/cucumber

# Run all scenarios
npx cucumber-js

# Run specific feature
npx cucumber-js claude_tasks/behaviors/features/my_feature.feature

# Generate HTML report
npx cucumber-js --format html:claude_tasks/behaviors/reports/living_docs.html
```

## Integration with TDD

1. **Write BDD scenarios** describing business behavior
2. **Create step definitions** that call your application code
3. **Write unit tests** for the implementation details
4. **Implement the code** to make both BDD scenarios and unit tests pass
5. **Validate with stakeholders** using the generated reports

## Best Practices

- Keep scenarios focused on business outcomes
- Use consistent language across all features
- Include both happy path and error scenarios
- Write scenarios collaboratively with stakeholders
- Keep step definitions simple and reusable
- Generate living documentation regularly
- Review scenarios with business stakeholders
- Update scenarios when requirements change
"""
        
        behaviors_readme_file = self.claude_tasks_dir / "behaviors" / "README.md"
        if not behaviors_readme_file.exists() or self.force:
            behaviors_readme_file.write_text(behaviors_readme_content)
            print(f"📄 Created: behaviors/README.md")
    
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
        if "claude_tasks" in existing_content and "BDD+TDD" in existing_content:
            print("✓ CLAUDE.md already references BDD+TDD task system")
            return
        elif "claude_tasks" in existing_content:
            print("🔄 Updating CLAUDE.md to include BDD methodology")
        
        # Prepend reference section
        reference_section = """# CLAUDE.md

## 📋 Claude Development Process
This project uses the Claude Task Management System with BDD+TDD methodology for AI-assisted development.

### Key Documents
- `claude_tasks/QUICK_REFERENCE.md` - Quick commands and BDD+TDD workflow
- `claude_tasks/BDD_PROCESS.md` - Complete 9-step methodology
- `claude_tasks/PRINCIPLES_QUICK_CARD.md` - Core development principles
- `claude_tasks/active/ACTIVE_TASKS.md` - Current task tracking
- `claude_tasks/behaviors/` - BDD specifications and living documentation

### Development Workflow
SPECIFY → RED → GREEN → REFACTOR → VALIDATE

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
        print("✅ Updated CLAUDE.md with BDD+TDD task system reference")
    
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

This project follows the Claude Task Management System with BDD+TDD methodology:
- Behavior-Driven Development (BDD) for stakeholder alignment
- Test-Driven Development (TDD) for technical implementation
- Structured task tracking and documentation
- AI-aware development patterns

### Key Documents
- `claude_tasks/QUICK_REFERENCE.md` - Quick commands and BDD+TDD workflow
- `claude_tasks/BDD_PROCESS.md` - Complete 9-step methodology
- `claude_tasks/PRINCIPLES_QUICK_CARD.md` - Core development principles
- `claude_tasks/active/ACTIVE_TASKS.md` - Current task tracking
- `claude_tasks/behaviors/` - BDD specifications and scenarios

## Core Development Principles

1. **Test Driven Development** - Write tests first, no code without tests
2. **Fail Fast & Root Cause** - Fix problems at their source, no workarounds
3. **Modular & Maintainable** - Single responsibility, decoupled components
4. **Reuse Before Build** - Check existing code and libraries first
5. **Open Source First** - Suggest alternatives before building new
6. **No Legacy Baggage** - Start clean, avoid technical debt
7. **Perfectionist Excellence** - Build best-of-breed solutions only

## Repository Overview

[TODO: Add project description]

## Project Structure

```
[TODO: Document structure]
├── claude_tasks/
│   ├── behaviors/           # BDD specifications
│   │   ├── features/       # Gherkin feature files
│   │   ├── step_definitions/ # Test implementations
│   │   └── reports/        # Living documentation
│   ├── active/             # Current tasks
│   └── finished/           # Completed tasks
├── tests/                  # Unit and integration tests
└── src/                    # Implementation code
```

## Common Development Commands

### Testing
```bash
# Run unit tests
npm test  # or appropriate command

# Run BDD scenarios
npx cucumber-js

# With coverage
npm test -- --coverage

# Watch mode for TDD
npm test -- --watch

# Generate living documentation
npx cucumber-js --format html:claude_tasks/behaviors/reports/living_docs.html
```

## Working with this Codebase

### BDD+TDD Workflow (9 Steps)
1. **CHECK** → Current state and active tasks
2. **SPECIFY** → Write behavior specifications in Gherkin
3. **PLAN** → Update tasks with behaviors to implement
4. **RED** → Write failing tests from specifications
5. **GREEN** → Write minimal code to pass tests
6. **REFACTOR** → Improve code quality
7. **VALIDATE** → Confirm behaviors work as specified
8. **DOCUMENT** → Record implementation and behaviors
9. **COMMIT** → Save with BDD+TDD message

### Task Management
- New tasks go in `claude_tasks/active/ACTIVE_TASKS.md`
- Write Gherkin scenarios in `claude_tasks/behaviors/features/`
- Completed tasks move to `claude_tasks/finished/`
- Follow the enhanced task template with behavior specifications

### AI-Specific Development
- Include model accuracy validation scenarios
- Test for bias detection and mitigation
- Implement human-in-loop validation workflows
- Document regulatory compliance behaviors
- Test edge cases and error conditions

See `claude_tasks/` for detailed methodology and `claude_tasks/behaviors/README.md` for BDD guidance.
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
            print(f"{step_num}. Review claude_tasks/QUICK_REFERENCE.md for BDD+TDD workflow")
            step_num += 1
            print(f"{step_num}. Read claude_tasks/BDD_PROCESS.md for complete 9-step methodology")
            step_num += 1
            print(f"{step_num}. Read claude_tasks/PRINCIPLES_QUICK_CARD.md for principles")
            step_num += 1
            print(f"{step_num}. Add your first task to claude_tasks/active/ACTIVE_TASKS.md")
            step_num += 1
            print(f"{step_num}. Create behavior scenarios in claude_tasks/behaviors/features/")
            step_num += 1
        
        if claude_md_exists:
            print(f"{step_num}. Customize CLAUDE.md with project-specific information")
            step_num += 1
        
        # Only suggest git commit if something was actually installed
        if claude_tasks_exists or claude_md_exists:
            print(f"{step_num}. Commit the changes: git add . && git commit -m 'Add Claude task management system'")
            step_num += 1
        
        if claude_tasks_exists:
            print("\n🎯 Start with BDD+TDD: cat claude_tasks/BDD_PROCESS.md")
            print("📝 Example behaviors: cat claude_tasks/behaviors/README.md")


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