# /stage - TDD Staging Pipeline

Execute complete staging pipeline: regression testing, approval confirmation, and version tagging for release preparation.

## Command Purpose

Comprehensive staging process that ensures code quality and prepares for release:
1. Run full regression testing (calls `/regression`)
2. Validate all quality gates pass
3. Confirm staging approval
4. Create and tag version number
5. Prepare release artifacts

## Implementation Steps

1. **Pre-Stage Validation**
   - Check git status (no uncommitted changes)
   - Validate current branch (typically `main` or `develop`)
   - Ensure working directory is clean

2. **Regression Testing**
   - Execute `/regression` command
   - Block progression if any quality gates fail
   - Require all tests passing + coverage >80%

3. **Version Management**
   - Read current version from version files (package.json, pyproject.toml, etc.)
   - Prompt for version bump type: patch/minor/major
   - Generate new version number following semver
   - Update version files across all projects

4. **Approval Confirmation**
   - Display staging summary with test results
   - Show version changes and affected projects
   - Require explicit human approval to proceed
   - Log approval decision with timestamp

5. **Git Tagging**
   - Commit version updates with standardized message
   - Create annotated git tag with version and metadata
   - Push tag to remote repository

## Example Usage

```bash
# Interactive staging with prompts
/stage

# Auto-patch version bump
/stage --version-bump patch

# Include specific projects only
/stage --projects "psychicblob,c4h_ai_dev"

# Skip confirmation for CI/CD
/stage --auto-approve --version-bump patch
```

## Staging Workflow

```
📋 TDD Staging Pipeline
======================

1. 🔍 Pre-stage validation...
   ✅ Git status clean
   ✅ On main branch
   ✅ No uncommitted changes

2. 🧪 Running regression tests...
   ✅ All projects: 189/189 tests passing
   ✅ Coverage: 87% average across projects
   ✅ No lint errors

3. 📦 Version management...
   Current: v1.2.3
   Proposed: v1.2.4 (patch)
   
   Projects to update:
   - ai_init: 1.2.3 → 1.2.4
   - psychicblob: 2.1.0 → 2.1.1
   - ai_mfe_portal: 1.0.2 → 1.0.3

4. ✅ Approval required:
   
   Proceed with staging v1.2.4? [y/N]: y
   
5. 🏷️  Creating release tag...
   ✅ Version files updated
   ✅ Git tag v1.2.4 created
   ✅ Changes pushed to origin

✅ STAGING COMPLETE
Ready for release deployment via /release command.
```

## Quality Gates

**BLOCKING CONDITIONS:**
- Any failing regression tests
- Code coverage below 80%
- Uncommitted git changes
- Lint/type errors
- Missing approval confirmation

**SUCCESS CRITERIA:**
- All tests passing
- Coverage thresholds met
- Clean git history
- Signed release tag created
- Version artifacts updated

## Integration with Release

The `/stage` command prepares artifacts for `/release`:
- Creates release tag with metadata
- Updates all project versions consistently  
- Validates deployment readiness
- Generates release notes from git history

## Technical Implementation

- Integrates with existing `/regression` command
- Uses semantic versioning (semver) standards
- Supports multiple project types (Node.js, Python)
- Creates standardized git tags with metadata
- Validates git repository state before/after operations