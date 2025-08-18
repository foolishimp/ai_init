# /stage - AI Init Staging Pipeline

Execute complete staging pipeline for ai_init framework: regression testing, quality validation, version management, and release preparation.

## Command Purpose

Comprehensive staging process that ensures ai_init framework quality and prepares for ecosystem-wide deployment:
1. Run full regression testing across all projects (calls `/regression`)
2. Validate all quality gates pass
3. Confirm staging approval with ecosystem impact assessment
4. Create and tag version number with framework metadata
5. Prepare release artifacts and deployment manifests

## Implementation Steps

1. **Pre-Stage Validation**
   - Check git status of ai_init repository (no uncommitted changes)
   - Validate current branch (typically `main`)
   - Ensure working directory is clean
   - Verify no pending tasks in `claude_tasks/active/ACTIVE_TASKS.md`

2. **Cross-Project Regression Testing**
   - Execute `/regression` command across all ai_init installations
   - Block progression if any critical quality gates fail
   - Require all framework tests passing + coverage >80%
   - Validate BDD scenarios across ecosystem
   - Ensure test dashboard integration functional

3. **AI Init Version Management**
   - Read current version from `VERSION` file and `package.json`
   - Analyze commit history for change impact (breaking/feature/patch)
   - Prompt for version bump type: patch/minor/major
   - Generate new version number following semantic versioning
   - Update version files: `VERSION`, `package.json`, `CHANGELOG.md`

4. **Ecosystem Impact Assessment**
   - Analyze projects that will be affected by framework changes
   - Identify breaking changes requiring project updates
   - Calculate deployment order based on dependencies
   - Generate upgrade compatibility matrix
   - Estimate rollout timeline across projects

5. **Approval Confirmation**
   - Display comprehensive staging summary with ecosystem impact
   - Show version changes and affected projects
   - Present BDD scenario compliance status
   - Require explicit human approval to proceed
   - Log approval decision with timestamp and impact scope

6. **Release Artifact Creation**
   - Commit version updates with standardized message
   - Create annotated git tag with framework metadata
   - Generate release notes from git history and CHANGELOG
   - Create deployment manifest for multi-project rollout
   - Prepare upgrade instructions for affected projects

## Example Usage

```bash
# Interactive staging with full ecosystem analysis
/stage

# Auto-patch version bump (for bug fixes)
/stage --version-bump patch

# Major version bump (for breaking changes like BDD integration)
/stage --version-bump major

# Include specific impact analysis
/stage --analyze-impact --projects "psychicblob,c4h_editor,ai_mfe_portal"

# Skip confirmation for CI/CD (requires pre-approval)
/stage --auto-approve --version-bump patch
```

## Staging Workflow

```
🚀 AI Init Framework Staging Pipeline
====================================

1. 🔍 Pre-stage validation...
   ✅ Git status clean (ai_init repository)
   ✅ On main branch
   ✅ No uncommitted changes
   ✅ No pending tasks in claude_tasks/active/

2. 🧪 Cross-project regression testing...
   ✅ Found 8 projects with ai_init installations
   ✅ Framework tests: 347/347 tests passing across ecosystem
   ✅ BDD scenarios: 89/92 scenarios passing (3 pending in 1 project)
   ✅ Average coverage: 87% across all projects
   ✅ Test dashboards: All functional on allocated ports
   ⚠️  1 project (c4h) using older framework version

3. 📦 AI Init version management...
   Current: v2.0.0
   Proposed: v2.1.0 (minor - new DevOps commands)
   
   Changes in this release:
   - Added /regression, /stage, /release commands
   - Enhanced cross-project testing capabilities
   - Improved ecosystem management features
   
4. 🌐 Ecosystem impact assessment...
   
   Projects affected by framework update:
   - psychicblob: ✅ Compatible (no changes needed)
   - ai_project_eval: ✅ Compatible (no changes needed)
   - c4h_editor: ✅ Compatible (no changes needed)
   - ai_mfe_portal: ✅ Compatible (no changes needed)
   - c4h: ⚠️  Requires upgrade from v1.x → v2.1.0
   - c4h_ai_dev: ✅ Compatible (no changes needed)
   - claude_dev: ✅ Compatible (no changes needed)
   - emergent_reasoning: ✅ Compatible (documentation only)

   Deployment strategy:
   - Phase 1: Update ai_init framework (safe, no breaking changes)
   - Phase 2: Deploy to compatible projects (automated)
   - Phase 3: Manual upgrade c4h project (requires BDD migration)

5. ✅ Staging approval required:
   
   📋 STAGING SUMMARY:
   - Framework version: v2.0.0 → v2.1.0
   - Projects affected: 8 total (7 compatible, 1 needs upgrade)
   - Breaking changes: None
   - New features: DevOps command system
   - Estimated rollout time: 30 minutes + 1 manual upgrade
   
   Proceed with staging ai_init v2.1.0? [y/N]: y
   
6. 🏷️  Creating release artifacts...
   ✅ Version files updated (VERSION, package.json, CHANGELOG.md)
   ✅ Git tag v2.1.0 created with framework metadata
   ✅ Release notes generated from commit history
   ✅ Deployment manifest created: deployment-manifest-v2.1.0.json
   ✅ Changes committed and tagged

✅ STAGING COMPLETE
AI Init v2.1.0 ready for ecosystem deployment via /release command.

Next steps:
1. Review deployment manifest: cat deployment-manifest-v2.1.0.json
2. Execute deployment: /release --manifest deployment-manifest-v2.1.0.json
3. Monitor rollout: /health --post-deployment
```

## Quality Gates

**BLOCKING CONDITIONS:**
- Any failing regression tests across ecosystem
- Critical BDD scenarios failing
- Framework functionality issues
- Code coverage below 80% in any project
- Uncommitted changes in ai_init repository
- Missing approval confirmation

**SUCCESS CRITERIA:**
- All cross-project tests passing
- BDD scenario compliance >95%
- Framework compatibility validated
- Clean git history in ai_init
- Signed release tag created with metadata
- Deployment manifest generated

## Framework-Specific Validations

**AI Init Framework Health:**
- Task management system functionality across all projects
- BDD+TDD methodology compliance
- Test dashboard integration and port management
- Living documentation generation capability
- Cross-project consistency validation

**Version Compatibility:**
- Breaking change detection
- Migration path identification
- Upgrade requirement analysis
- Rollback capability validation

## Integration with Release

The `/stage` command prepares comprehensive artifacts for `/release`:
- Creates framework release tag with ecosystem metadata
- Generates deployment manifest with project-specific instructions
- Validates deployment readiness across entire ecosystem
- Provides rollback information and upgrade guidance
- Creates automated deployment scripts for compatible projects

## Technical Implementation

- Integrates with existing `/regression` command for ecosystem testing
- Uses semantic versioning with framework-specific metadata
- Generates deployment manifests in JSON format
- Creates standardized git tags with ecosystem impact data
- Validates ai_init repository state before/after operations
- Manages cross-project dependency analysis

## Deployment Manifest Format

```json
{
  "ai_init_version": "2.1.0",
  "release_date": "2025-01-18T14:30:00Z",
  "staged_by": "claude",
  "ecosystem_status": {
    "total_projects": 8,
    "compatible_projects": 7,
    "requires_upgrade": 1,
    "breaking_changes": false
  },
  "deployment_phases": [
    {
      "phase": 1,
      "description": "Framework update",
      "projects": ["ai_init"],
      "automated": true,
      "estimated_time": "5 minutes"
    },
    {
      "phase": 2,
      "description": "Compatible project deployment",
      "projects": ["psychicblob", "ai_project_eval", "c4h_editor", "ai_mfe_portal", "c4h_ai_dev", "claude_dev"],
      "automated": true,
      "estimated_time": "20 minutes"
    },
    {
      "phase": 3,
      "description": "Manual upgrade required",
      "projects": ["c4h"],
      "automated": false,
      "upgrade_guide": "docs/upgrade-v1-to-v2.md",
      "estimated_time": "manual intervention required"
    }
  ],
  "rollback_plan": {
    "enabled": true,
    "restore_version": "2.0.0",
    "automatic_rollback": "phase_1_and_2_only"
  }
}
```