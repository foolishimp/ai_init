# /regression - AI Init Cross-Project Regression Testing

Run comprehensive regression test suite across all projects using ai_init to ensure framework quality and compatibility before releases.

## Command Purpose

Execute comprehensive regression testing following BDD+TDD methodology across all ai_init installations to validate:
- Unit test coverage (>80% required across all projects)
- Integration test functionality with ai_init framework
- BDD scenario validation
- Test dashboard functionality
- Build pipeline health across projects
- ai_init framework compatibility

## Implementation Steps

1. **Discover AI Init Projects**
   - Scan `/Users/jim/src/apps/` for projects with ai_init installations
   - Identify projects with `claude_tasks/` directories
   - Check for `test_dd_dashboard/` integration
   - Read project-specific CLAUDE.md for custom test commands

2. **Execute Project Test Suites**
   - For each Node.js project: `npm test`, `npm run test:coverage`
   - For each Python project: `python -m pytest --cov=. --cov-report=term-missing`
   - Run BDD scenarios: `npx cucumber-js claude_tasks/behaviors/features/`
   - Execute ai_init specific tests: validate task management, BDD workflow
   - Capture test results, coverage metrics, and failure details

3. **AI Init Framework Validation**
   - Verify Claude task management system functionality
   - Test BDD+TDD 9-step workflow compliance
   - Validate behavior specifications and living documentation
   - Check test dashboard integration and categorization
   - Verify version compatibility across installations

4. **Test Dashboard Aggregation**
   - Start test dashboards for each project on incremental ports
   - Aggregate results from all project dashboards
   - Validate cross-project test categorization consistency
   - Generate unified test metrics across ai_init ecosystem

5. **Quality Gates Validation**
   - **PASS Criteria**: All tests passing + coverage >80% + BDD scenarios pass + ai_init framework functional
   - **WARN Criteria**: Tests passing but coverage <80% or BDD scenarios incomplete
   - **FAIL Criteria**: Any failing tests, build errors, or ai_init framework issues

6. **Ecosystem Health Report**
   - Project-by-project ai_init health status
   - Framework version compatibility matrix
   - Cross-project test coverage summary
   - BDD scenario compliance report
   - Recommendations for framework updates

## Example Usage

```bash
# Basic regression run across all ai_init projects
/regression

# With specific project filter
/regression --projects "psychicblob,ai_project_eval,c4h_editor"

# Include BDD scenario validation
/regression --include-bdd

# Focus on ai_init framework tests only
/regression --framework-only

# Generate detailed ecosystem report
/regression --report-format detailed --output ecosystem-health.md
```

## Output Format

```
🔄 AI Init Ecosystem Regression Testing
=======================================

📊 AI Init Project Discovery:
✅ Found 8 projects with ai_init installations
✅ All projects have claude_tasks/ framework
⚠️  2 projects missing BDD behaviors/ directory
✅ 6 projects have test dashboard integration

🧪 Framework Testing Results:
✅ psychicblob: 186/186 tests passing (94% coverage) + 12/12 BDD scenarios ✅
❌ ai_project_eval: 0/5 tests failing (evaluation framework errors)  
⚠️  c4h_editor: 45/50 tests passing (integration timeouts) + 8/10 BDD scenarios ⚠️
✅ ai_mfe_portal: 23/23 tests passing (87% coverage) + 15/15 BDD scenarios ✅
❌ c4h: Framework compatibility issues (v1.x vs v2.x)
✅ c4h_ai_dev: 34/34 tests passing (91% coverage) + 6/6 BDD scenarios ✅
✅ claude_dev: 12/12 tests passing (89% coverage) + 4/4 BDD scenarios ✅
⚠️  emergent_reasoning: No tests configured (documentation project)

📋 AI Init Framework Health:
✅ 5/8 projects fully compliant with BDD+TDD v2.0
⚠️  2/8 projects need framework upgrade
❌ 1/8 projects have compatibility issues

🎯 Quality Gates Status:
❌ FAIL: 2 projects with failing tests
⚠️  WARN: 2 projects need BDD implementation
⚠️  WARN: 1 project needs framework upgrade
✅ PASS: 5 projects meet all criteria

📊 Cross-Project Metrics:
- Average test coverage: 87%
- BDD scenario compliance: 75%
- Framework version compatibility: 63%
- Test dashboard integration: 75%

📋 Required Actions Before Release:
1. Fix ai_project_eval evaluation framework errors
2. Resolve c4h_editor integration timeouts
3. Upgrade c4h to ai_init v2.0 (BDD+TDD)
4. Add BDD behaviors to 2 projects missing scenarios
5. Configure tests for emergent_reasoning if applicable

❌ REGRESSION STATUS: BLOCKED
Cannot proceed to staging until critical issues resolved.

Next Steps:
1. Run '/fix ai_project_eval c4h' to address failing projects
2. Run '/upgrade c4h' to update framework version
3. Re-run '/regression' to validate fixes
4. Proceed to '/stage' when all quality gates pass
```

## Integration with BDD+TDD Workflow

This command enforces the enhanced ai_init methodology:
- **CHECK**: Validate current state across all projects
- **SPECIFY**: Ensure BDD scenarios are present and passing
- **RED/GREEN/REFACTOR**: Verify TDD compliance across ecosystem
- **VALIDATE**: Confirm behavior specifications work as intended

Blocks progression to `/stage` command if quality gates fail.

## AI Init Specific Validations

**Framework Functionality Tests:**
- Task management system (`claude_tasks/active/ACTIVE_TASKS.md` functionality)
- BDD workflow (`behaviors/features/` execution)
- Test dashboard integration (port allocation, test discovery)
- Documentation generation (living docs from BDD scenarios)
- Version compatibility across projects

**Cross-Project Consistency:**
- Methodology compliance (9-step BDD+TDD process)
- File structure standardization
- Command availability (slash commands)
- Test categorization consistency

## Technical Implementation

- Use `subprocess` to execute test commands across projects
- Parse ai_init specific configuration files (`claude_tasks/`, `behaviors/`)
- Integrate with existing test dashboard infrastructure
- Store results in standardized format for `/stage` command consumption
- Generate unified ecosystem health metrics
- Validate framework version compatibility

## Error Handling

**Common Failure Scenarios:**
- Projects with outdated ai_init versions
- Missing BDD implementation in some projects
- Test dashboard port conflicts
- Framework integration failures

**Recovery Guidance:**
- Automated suggestions for fixing common issues
- Framework upgrade recommendations
- Port conflict resolution
- Integration repair instructions