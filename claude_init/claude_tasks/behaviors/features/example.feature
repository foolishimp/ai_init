Feature: Example AI Project Behavior
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