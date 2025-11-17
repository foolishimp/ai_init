# /finish - Complete Active Tasks and Commit

Complete all active tasks according to the BDD+TDD methodology, create finished task documentation, and perform a git commit with proper formatting.

## Command Purpose

Execute the complete task finishing workflow as defined in QUICK_REFERENCE.md:
1. Document completed tasks in finished files with test metrics
2. Remove completed tasks from active list
3. Create comprehensive git commit with TDD message format
4. Archive any working documents

## Implementation Steps

1. **Read Active Tasks**
   - Load `claude_tasks/active/ACTIVE_TASKS.md`
   - Identify all tasks marked as "Completed" or "In Progress" that are ready to finish
   - Parse task details including ID, title, description, and acceptance criteria

2. **Create Finished Task Files**
   - For each completed task, create: `claude_tasks/finished/YYYYMMDD_HHMM_task_name.md`
   - Use completion timestamp in filename
   - Follow TDD finished task template with required sections:
     - Problem and Solution sections
     - Test Coverage metrics (unit/integration/e2e)
     - Feature Flag status
     - Files Modified with TDD process (RED→GREEN→REFACTOR)
     - TDD Process Notes

3. **Update Active Tasks**
   - Remove completed tasks from `claude_tasks/active/ACTIVE_TASKS.md`
   - Keep any remaining "Not Started" or "In Progress" tasks
   - Maintain proper formatting and task numbering

4. **Analyze Test Coverage**
   - Run test coverage analysis if test commands are available
   - Extract coverage percentage for inclusion in finished files
   - Document test counts by category (unit, integration, e2e)

5. **Feature Flag Management**
   - Check for any feature flags related to completed tasks
   - Document current flag status in finished files
   - Provide recommendations for flag defaultValue updates

6. **Git Commit with TDD Format**
   - Stage all changes including finished files and active task updates
   - Create commit message following exact format from QUICK_REFERENCE.md:
     ```
     Task #N: [Title from finished task]
     
     [Problem section content from finished file]
     
     [Solution section content from finished file]
     
     Tests: X unit, X integration, X E2E | Coverage: XX%
     TDD: RED → GREEN → REFACTOR
     
     🤖 Generated with [Claude Code](https://claude.ai/code)
     Co-Authored-By: Claude <noreply@anthropic.com>
     ```

## Example Usage

```bash
# Finish all completed active tasks
/finish

# Finish specific task by ID
/finish --task 5

# Finish with custom commit message addition
/finish --note "Fixed critical bug in authentication"

# Dry run to see what would be finished
/finish --dry-run
```

## Workflow Example

```
🏁 Task Completion Workflow
==========================

📋 Reading active tasks...
   ✅ Found 2 completed tasks ready to finish:
   - Task #15: Implement user authentication
   - Task #16: Add password validation

📝 Creating finished task files...
   ✅ Created: claude_tasks/finished/20250118_1445_implement_user_authentication.md
   ✅ Created: claude_tasks/finished/20250118_1445_add_password_validation.md

🧪 Analyzing test coverage...
   ✅ Total Coverage: 87% (target: >80%)
   ✅ Unit Tests: 23 tests
   ✅ Integration Tests: 8 tests
   ✅ E2E Tests: 3 tests

🚩 Feature Flag Analysis...
   ✅ task-15-user-auth: Currently disabled (recommend enabling)
   ✅ task-16-password-validation: Currently disabled (recommend enabling)

📋 Updating active tasks...
   ✅ Removed 2 completed tasks from ACTIVE_TASKS.md
   ✅ 3 remaining active tasks

📦 Committing changes...
   ✅ Staged: claude_tasks/finished/ (2 files)
   ✅ Staged: claude_tasks/active/ACTIVE_TASKS.md
   ✅ Staged: src/ (modified files)

   Commit Message:
   ================
   Task #15-16: Implement user authentication with password validation
   
   Problem:
   Application needed secure user authentication system with robust password validation.
   
   Solution:
   Implemented JWT-based authentication with bcrypt password hashing and comprehensive 
   validation including strength requirements, entropy checking, and common password detection.
   
   Tests: 23 unit, 8 integration, 3 E2E | Coverage: 87%
   TDD: RED → GREEN → REFACTOR
   
   🤖 Generated with [Claude Code](https://claude.ai/code)
   Co-Authored-By: Claude <noreply@anthropic.com>

✅ TASK COMPLETION SUCCESSFUL
   2 tasks documented and committed successfully.
   
   Next Steps:
   1. Consider enabling feature flags for completed features
   2. Review remaining 3 active tasks
   3. Run deployment pipeline if needed
```

## Configuration Options

**Task Selection:**
- **All Completed**: Finish all tasks marked as completed
- **Specific Task**: Target individual task by ID
- **In Progress**: Optionally include "In Progress" tasks that are ready
- **Interactive**: Prompt for confirmation before finishing each task

**Documentation Options:**
- **Test Coverage**: Include detailed test metrics from coverage reports
- **Feature Flags**: Analyze and document related feature flag status
- **File Analysis**: List all modified files with their changes
- **TDD Process**: Document RED→GREEN→REFACTOR progression

**Commit Options:**
- **Multi-Task Commit**: Combine multiple finished tasks in single commit
- **Individual Commits**: Create separate commit for each finished task
- **Dry Run**: Show what would be committed without making changes
- **Custom Notes**: Add additional context to commit message

## Integration with BDD+TDD Workflow

This command enforces the complete BDD+TDD finishing methodology:
- **VALIDATE**: Confirms behavior specifications worked as intended
- **DOCUMENT**: Creates comprehensive finished task records
- **TEST**: Includes test coverage and TDD process documentation
- **COMMIT**: Uses standardized commit message format
- **ARCHIVE**: Moves completed work to finished directory

## Technical Implementation

**File Operations:**
- Parse ACTIVE_TASKS.md for completed tasks
- Generate timestamped finished task files
- Update active tasks file with remaining work
- Handle git staging and commit operations

**Test Integration:**
- Execute test coverage commands if available
- Parse coverage reports for metrics
- Document test counts by category
- Validate minimum coverage thresholds

**Feature Flag Integration:**
- Scan code for feature flags related to completed tasks
- Document current flag status and recommendations
- Provide guidance for flag lifecycle management

## Safety Features

**Validation Checks:**
- Verify all completed tasks have proper acceptance criteria met
- Ensure minimum test coverage thresholds (>80%)
- Validate that no critical files are uncommitted
- Check for any TODO/FIXME comments related to completed tasks

**Backup and Recovery:**
- Create backup of ACTIVE_TASKS.md before modification
- Store original task content in finished files
- Provide rollback instructions if commit needs to be undone
- Maintain task traceability through ID system

**Error Handling:**
- Handle missing test commands gracefully
- Provide clear error messages for validation failures
- Support partial completion if some tasks can't be finished
- Offer recovery suggestions for common issues

## Best Practices Enforcement

This command enforces all QUICK_REFERENCE.md best practices:
- **One Task, One Purpose**: Documents exactly what each task accomplished
- **Clear Documentation**: Creates detailed finished task records
- **Test Coverage**: Validates >80% coverage requirement
- **TDD Process**: Documents RED→GREEN→REFACTOR progression
- **Feature Flags**: Manages feature flag lifecycle properly
- **Commit Discipline**: Uses standardized commit message format
- **Traceability**: Maintains clear audit trail of completed work