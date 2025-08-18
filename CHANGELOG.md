# Changelog

All notable changes to the ai_init framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-01-18

### Added
- **DevOps Command System**: Comprehensive CI/CD commands for ecosystem management
- **Cross-Project Regression Testing**: `/regression` command for framework validation
- **Staging Pipeline**: `/stage` command with version management and quality gates
- **Ecosystem Deployment**: `/release` command for coordinated multi-project rollout
- **Version Management**: Semantic versioning with deployment manifest generation
- **Quality Gates**: Automated quality validation across all ai_init installations

### New Commands
- `/regression` - Cross-project regression testing with BDD validation
- `/stage` - Complete staging pipeline with ecosystem impact assessment
- `/release` - Phased deployment across entire project ecosystem

### DevOps Features
- **Deployment Manifests**: JSON-based deployment configuration with phased rollout
- **Backup and Recovery**: Automated backup creation with selective restoration
- **Health Monitoring**: Pre/post-deployment validation and ecosystem health checks
- **Port Management**: Dynamic port allocation for test dashboard instances
- **Framework Compatibility**: Version compatibility validation across projects

### Integration
- **Meta-Project Support**: Direct integration with multi-project development
- **Test Dashboard**: Enhanced cross-project test aggregation
- **Git Integration**: Automated tagging and release management
- **Ecosystem Coordination**: Unified deployment across ai_init installations

## [2.0.0] - 2025-01-18

### Added
- **BDD Integration**: Complete Behavior-Driven Development framework
- **9-Step BDD+TDD Process**: Enhanced from 7-step TDD to comprehensive methodology
- **Gherkin Templates**: AI-specific scenario examples for model validation, bias detection
- **Living Documentation**: Automated behavior documentation generation
- **Stakeholder Collaboration**: Business-readable specifications in Gherkin format

### New Files
- `claude_tasks/BDD_PROCESS.md` - Complete 9-step BDD+TDD methodology
- `claude_tasks/behaviors/` - BDD specifications directory structure
- `claude_tasks/behaviors/features/example.feature` - AI scenario templates
- `claude_tasks/behaviors/step_definitions/common_steps.js` - Step implementations
- `claude_tasks/behaviors/README.md` - BDD guidance and best practices

### Enhanced
- **QUICK_REFERENCE.md**: Updated to 9-step workflow with BDD commands
- **PRINCIPLES_QUICK_CARD.md**: Added BDD principles and updated mantras
- **ACTIVE_TASKS.md**: Enhanced template with behavior specifications
- **setup_claude_tasks.py**: Added BDD directory creation and file copying
- **setup_all.py**: Updated descriptions to mention BDD+TDD capabilities

### Changed
- **Development Workflow**: SPECIFY → RED → GREEN → REFACTOR → VALIDATE
- **Task Templates**: Now include behavior specifications and stakeholder validation
- **Commit Messages**: Enhanced format includes both behavior and technical details

### AI-Specific Features
- Model accuracy validation scenarios
- Bias detection and mitigation workflows
- Human-in-loop validation processes
- Regulatory compliance behaviors
- Confidence threshold testing patterns

## [1.x.x] - Previous Versions
- TDD-only framework
- 7-step development process
- Test dashboard integration
- Claude task management system