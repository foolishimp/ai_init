# BDD+TDD Development Process

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