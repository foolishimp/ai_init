# /release - AI Init Ecosystem Deployment

Deploy ai_init framework updates across the entire project ecosystem using staged release manifests and automated rollout procedures.

## Command Purpose

Execute controlled, phased deployment of ai_init framework to all projects in the ecosystem:
1. Validate staging artifacts and deployment readiness
2. Execute phased deployment to compatible projects
3. Coordinate manual upgrades for projects requiring migration
4. Monitor deployment health and provide rollback capability
5. Update ecosystem documentation and deployment logs

## Implementation Steps

1. **Release Validation**
   - Verify latest deployment manifest exists from `/stage` command
   - Confirm staging tag is properly signed with ecosystem metadata
   - Validate that all quality gates passed during staging
   - Check deployment manifest integrity and phase definitions

2. **Project Discovery and Validation**
   - Scan ecosystem for all projects with ai_init installations
   - Validate each project directory exists and is accessible
   - Check for existing ai_init installations and version compatibility
   - Identify projects requiring manual intervention vs. automated deployment

3. **Phased Deployment Execution**
   - **Phase 1**: Framework repository update (ai_init itself)
   - **Phase 2**: Automated deployment to compatible projects
   - **Phase 3**: Guided manual upgrades for projects requiring migration
   - Execute each phase with validation and rollback checkpoints

4. **Automated Project Updates**
   - For each compatible project:
     - Backup existing ai_init configuration
     - Run `python ai_init/setup_all.py --target <project_path> --force`
     - Validate successful installation and framework functionality
     - Update project CLAUDE.md with new framework version
     - Test basic functionality (task management, test dashboard)

5. **Manual Upgrade Coordination**
   - For projects requiring manual intervention:
     - Generate project-specific upgrade guides
     - Provide step-by-step migration instructions
     - Offer rollback procedures if upgrade fails
     - Validate successful migration before marking complete

6. **Post-Deployment Validation**
   - Verify ai_init framework functionality across all projects
   - Test cross-project regression compatibility
   - Validate BDD+TDD workflow functionality
   - Ensure test dashboard integration works on allocated ports
   - Generate ecosystem health report

## Example Usage

```bash
# Deploy using latest staging manifest
/release

# Deploy with specific manifest file
/release --manifest deployment-manifest-v2.1.0.json

# Deploy to specific projects only
/release --projects "psychicblob,ai_project_eval,c4h_editor"

# Execute specific deployment phase
/release --phase 2 --manifest deployment-manifest-v2.1.0.json

# Dry-run to see deployment plan without execution
/release --dry-run --manifest deployment-manifest-v2.1.0.json

# Force deployment with automated rollback on failure
/release --auto-rollback --manifest deployment-manifest-v2.1.0.json
```

## Release Workflow

```
🚀 AI Init Ecosystem Deployment
===============================

📋 Release Information:
   Framework Version: v2.1.0 (from staging manifest)
   Deployment Manifest: deployment-manifest-v2.1.0.json
   Staged Date: 2025-01-18 14:30:00
   Total Projects: 8

🔍 Pre-deployment validation...
   ✅ Deployment manifest validated
   ✅ Staging tag v2.1.0 exists and verified
   ✅ All target projects accessible
   ✅ No blocking quality gate failures

📦 PHASE 1: Framework Repository Update
   🎯 Target: ai_init framework
   ✅ Framework updated to v2.1.0
   ✅ New DevOps commands available
   ✅ Repository integrity verified
   ⏱️  Completed in 2 minutes

📦 PHASE 2: Compatible Project Deployment
   🎯 Targets: 7 compatible projects
   
   📁 psychicblob:
   ✅ Backup created: /tmp/psychicblob-ai_init-backup-20250118
   ✅ Framework updated: v2.0.0 → v2.1.0
   ✅ Test dashboard functional (port: 8085)
   ✅ BDD workflows validated
   
   📁 ai_project_eval:
   ✅ Backup created: /tmp/ai_project_eval-ai_init-backup-20250118
   ✅ Framework updated: v2.0.0 → v2.1.0
   ✅ Test dashboard functional (port: 8086)
   ✅ Evaluation framework integration verified
   
   📁 c4h_editor:
   ✅ Backup created: /tmp/c4h_editor-ai_init-backup-20250118
   ✅ Framework updated: v2.0.0 → v2.1.0
   ✅ Test dashboard functional (port: 8087)
   ✅ Microfrontend integration preserved
   
   📁 ai_mfe_portal:
   ✅ Backup created: /tmp/ai_mfe_portal-ai_init-backup-20250118
   ✅ Framework updated: v2.0.0 → v2.1.0
   ✅ Test dashboard functional (port: 8088)
   ✅ Portal integration verified
   
   📁 c4h_ai_dev:
   ✅ Backup created: /tmp/c4h_ai_dev-ai_init-backup-20250118
   ✅ Framework updated: v2.0.0 → v2.1.0
   ✅ Test dashboard functional (port: 8089)
   ✅ AI development workflows preserved
   
   📁 claude_dev:
   ✅ Backup created: /tmp/claude_dev-ai_init-backup-20250118
   ✅ Framework updated: v2.0.0 → v2.1.0
   ✅ Test dashboard functional (port: 8090)
   ✅ Development documentation updated
   
   📁 emergent_reasoning:
   ✅ Backup created: /tmp/emergent_reasoning-ai_init-backup-20250118
   ✅ Framework updated: v2.0.0 → v2.1.0
   ✅ Documentation-only project, no test dashboard needed
   
   ⏱️  Phase 2 completed in 18 minutes

📦 PHASE 3: Manual Upgrade Required
   🎯 Target: c4h (requires v1.x → v2.1.0 migration)
   
   ⚠️  Manual intervention required for: c4h
   📋 Upgrade Guide: docs/upgrade-v1-to-v2.md
   🔧 Migration Steps:
   1. Backup existing framework: ✅ Done
   2. Install v2.1.0 framework: ⏸️  Pending manual execution
   3. Migrate to BDD+TDD methodology: ⏸️  Pending
   4. Update task templates: ⏸️  Pending
   5. Validate BDD scenarios: ⏸️  Pending
   
   📞 Manual Action Required:
   cd /Users/jim/src/apps/c4h
   python /Users/jim/src/apps/ai_init/setup_all.py --force
   # Follow migration guide for BDD integration
   
📊 Deployment Summary:
   ✅ Phase 1: Framework updated successfully
   ✅ Phase 2: 7/7 compatible projects deployed successfully
   ⏸️  Phase 3: 1 project pending manual upgrade
   
   📈 Success Rate: 87.5% (7/8 projects fully deployed)
   ⏱️  Total Time: 20 minutes automated + manual intervention pending

🔍 Post-deployment validation...
   ✅ Cross-project framework functionality verified
   ✅ Test dashboard port allocation successful (8085-8090)
   ✅ BDD+TDD workflows functional across deployed projects
   ✅ Living documentation generation working
   ✅ No regression failures detected

✅ DEPLOYMENT COMPLETE (AUTOMATED PHASES)
   AI Init v2.1.0 deployed to 7/8 projects successfully.
   
   📋 Next Steps:
   1. Complete manual upgrade for c4h project
   2. Run '/health --post-deployment' to validate ecosystem
   3. Update ecosystem documentation
   4. Monitor projects for 24 hours for any issues

📊 Ecosystem Status:
   - Framework Version: v2.1.0 deployed
   - Projects Updated: 7/8 (87.5%)
   - Manual Intervention: 1 project (c4h)
   - Rollback Available: Yes (automated phases only)
```

## Configuration Options

**Deployment Strategies:**
- **Automated Deployment**: For compatible projects with no breaking changes
- **Manual Upgrade**: For projects requiring framework migration
- **Phased Rollout**: Staged deployment with validation checkpoints
- **Rollback Capability**: Automatic restoration if deployment fails

**Safety Features:**
- Pre-deployment backup of all ai_init configurations
- Validation checkpoints between deployment phases
- Automatic rollback on critical failures
- Preservation of project-specific customizations
- Health monitoring throughout deployment process

## Integration with Staging

The `/release` command consumes artifacts from `/stage`:
- Uses deployment manifest created by staging pipeline
- Validates staging success and quality gates before deployment
- Maintains ecosystem consistency across phased rollout
- Links deployment to specific tested and approved release

## Error Handling and Recovery

**Common Failure Scenarios:**
- Project directory access issues
- Port conflicts for test dashboard allocation
- Framework integration failures
- Project-specific configuration conflicts
- Network or permission issues during deployment

**Recovery Actions:**
- **Automatic Rollback**: Restore previous framework version from backups
- **Partial Deployment**: Continue with successful projects, isolate failures
- **Manual Intervention**: Provide detailed error logs and recovery instructions
- **Health Monitoring**: Continuous validation during and after deployment

**Rollback Procedures:**
```bash
# Automatic rollback of last deployment
/release --rollback --manifest deployment-manifest-v2.1.0.json

# Rollback specific projects
/release --rollback --projects "c4h_editor,ai_mfe_portal"

# Restore from backup
/release --restore-backup --project psychicblob --backup-path /tmp/psychicblob-ai_init-backup-20250118
```

## Technical Implementation

**Deployment Engine:**
- Leverages existing `setup_all.py` infrastructure for project installation
- Manages port allocation across multiple test dashboard instances
- Integrates with git tagging system from `/stage` command
- Provides comprehensive logging and error reporting
- Supports both individual and batch deployments

**Validation Framework:**
- Pre-deployment readiness checks
- Post-deployment functionality validation
- Cross-project compatibility testing
- Framework integrity verification
- Ecosystem health monitoring

**Backup and Recovery:**
- Automated backup creation before any changes
- Versioned backup storage with metadata
- Selective restoration capabilities
- Configuration preservation across updates

## Ecosystem Documentation Updates

**Automated Documentation:**
- Update project CLAUDE.md files with new framework version
- Generate ecosystem-wide deployment log
- Create framework version compatibility matrix
- Update cross-project dependency documentation

**Manual Documentation:**
- Deployment summary with lessons learned
- Updated upgrade guides for future releases
- Ecosystem health metrics and trends
- Best practices based on deployment experience