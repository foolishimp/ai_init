# /release - AI Init Deployment to Projects

Deploy ai_init development tools to specified projects using the latest staged version tag.

## Command Purpose

Execute controlled deployment of ai_init tooling to target projects:
1. Validate staging tag exists and is latest
2. Deploy ai_init tools to specified project directories
3. Configure project-specific settings
4. Verify successful installation
5. Update project documentation

## Implementation Steps

1. **Release Validation**
   - Verify latest git tag exists from `/stage` command
   - Confirm tag is properly signed and contains metadata
   - Check that tag represents successful staging pipeline
   - Validate target project directories exist

2. **Project Selection**
   - Accept project list as command arguments
   - Validate each project directory exists
   - Check for existing ai_init installations
   - Confirm overwrite permissions if needed

3. **Deployment Execution**
   - For each target project:
     - Run `python ai_init/setup_all.py --target <project_path>`
     - Configure project-specific settings (ports, versions)
     - Install Claude Task Management System
     - Install Test Dashboard Module
     - Update project CLAUDE.md with release info

4. **Post-Deployment Validation**
   - Verify ai_init tools installed correctly
   - Test basic functionality (task management, test dashboard)
   - Validate project can execute TDD workflow
   - Check integration with existing project structure

5. **Documentation Updates**
   - Update project CLAUDE.md with ai_init version
   - Add release notes to project documentation
   - Create deployment log with timestamp and version
   - Update meta-level project tracking

## Example Usage

```bash
# Deploy to specific projects
/release --projects "claude_dev,psychicblob"

# Deploy with custom configuration
/release --projects "c4h_editor" --dashboard-port 3001

# Force reinstall over existing
/release --projects "ai_mfe_portal" --force

# Deploy to all projects with ai_init support
/release --all-supported

# Dry-run to see what would be deployed
/release --projects "claude_dev" --dry-run
```

## Release Workflow

```
🚀 AI Init Release Deployment
=============================

📋 Release Information:
   Version: v1.2.4
   Tag: Latest staged release
   Date: 2025-08-17 13:15:00

🎯 Target Projects:
   - claude_dev: /Users/jim/src/apps/claude_dev
   - psychicblob: /Users/jim/src/apps/psychicblob

🔍 Pre-deployment validation...
   ✅ Release tag v1.2.4 exists
   ✅ All target directories accessible
   ✅ Deployment permissions confirmed

📦 Deploying to claude_dev...
   ✅ Claude Task Management System installed
   ✅ Test Dashboard Module installed (port: 8085)
   ✅ Project CLAUDE.md updated
   ✅ Integration verified

📦 Deploying to psychicblob...
   ✅ Claude Task Management System updated
   ✅ Test Dashboard Module updated (port: 8086)
   ✅ Project configuration preserved
   ✅ Integration verified

📊 Deployment Summary:
   ✅ 2/2 projects deployed successfully
   ✅ All integrations verified
   ✅ Documentation updated

✅ RELEASE DEPLOYMENT COMPLETE
   AI Init v1.2.4 deployed to 2 projects.
```

## Configuration Options

**Project-Specific Settings:**
- Dashboard port assignment (auto-increment from 8085)
- Force reinstall vs. preserve existing configuration
- Custom installation options (claude-only, dashboard-only)
- Integration with existing project test frameworks

**Safety Features:**
- Backup existing configurations before deployment
- Rollback capability if deployment fails
- Validation of successful installation
- Preservation of project-specific customizations

## Integration with Staging

The `/release` command consumes artifacts from `/stage`:
- Uses latest git tag created by staging pipeline
- Validates staging success before deployment
- Maintains version consistency across deployments
- Links deployment to specific tested release

## Error Handling

**Common Failure Scenarios:**
- Target project directory doesn't exist
- Insufficient permissions for installation
- Port conflicts with existing services
- Integration failures with project structure

**Recovery Actions:**
- Automatic rollback of failed installations
- Detailed error reporting with resolution guidance
- Preservation of original project state
- Option to retry with different configuration

## Technical Implementation

- Leverages existing `setup_all.py` infrastructure
- Manages port allocation across multiple deployments
- Integrates with git tagging system from `/stage`
- Provides comprehensive logging and error reporting
- Supports both individual and batch deployments