# /regression - Comprehensive TDD Regression Testing

Run complete regression test suite across all projects in the meta-level ecosystem to ensure code quality before checkin.

## Command Purpose

Execute comprehensive regression testing following TDD methodology across all active projects to validate:
- Unit test coverage (>80% required)
- Integration test functionality 
- E2E workflow validation
- Build pipeline health
- Code quality metrics
- Dependency resolution

## Implementation Steps

1. **Discover Active Projects**
   - Scan `/Users/jim/src/apps/` for projects with test configurations
   - Identify Node.js projects (package.json with test scripts)
   - Identify Python projects (pytest/requirements.txt)
   - Read project-specific CLAUDE.md for test commands

2. **Execute Test Suites**
   - For each Node.js project: `npm test`, `npm run test:coverage`
   - For each Python project: `python -m pytest --cov=. --cov-report=term-missing`
   - Capture test results, coverage metrics, and failure details
   - Run linting and type checking where configured

3. **Test Dashboard Integration**
   - Start test dashboard: `PROJECT_DIRS="." node test-dashboard-module/server.js`
   - Validate all tests discoverable through dashboard
   - Check test categorization (Interface/Component/Integration/Performance/Unit)

4. **Quality Gates**
   - **PASS Criteria**: All tests passing + coverage >80% + no lint errors
   - **WARN Criteria**: Tests passing but coverage <80% or lint warnings
   - **FAIL Criteria**: Any failing tests or build errors

5. **Report Generation**
   - Create summary with project-by-project results
   - List failing tests with error details
   - Coverage report by project
   - Recommendations for fixes

## Example Usage

```bash
# Basic regression run
/regression

# With specific project filter
/regression --projects "psychicblob,c4h_ai_dev"

# Include performance benchmarks
/regression --include-performance

# Generate detailed report
/regression --report-format detailed
```

## Output Format

```
🔄 TDD Regression Testing Results
================================

📊 Project Summary:
✅ psychicblob: 186/216 tests passing (86% coverage)
❌ c4h_ai_dev: 0/24 tests passing (dependency errors)
⚠️  ai_mfe_portal: 3/5 tests passing (integration timeouts)
✅ c4h_editor: No tests configured

🎯 Quality Gates:
❌ FAIL: 2 projects with failing tests
⚠️  WARN: 1 project needs test configuration
✅ PASS: 1 project meets all criteria

📋 Required Actions:
1. Fix c4h_ai_dev dependency issues
2. Resolve ai_mfe_portal integration timeouts  
3. Add test script to c4h_editor

❌ REGRESSION STATUS: BLOCKED
Cannot proceed to staging until all tests pass.
```

## Integration with TDD Workflow

This command enforces the TDD quality gates:
- **RED**: Identify failing tests across projects
- **GREEN**: Ensure all tests pass before progression
- **REFACTOR**: Provide guidance for fixing issues

Blocks progression to `/stage` command if quality gates fail.

## Technical Implementation

- Use `subprocess` to execute test commands
- Parse test output for pass/fail/coverage metrics
- Integrate with existing test dashboard infrastructure
- Store results in standardized format for `/stage` command consumption