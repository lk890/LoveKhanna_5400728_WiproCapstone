Feature: Myntra Category Automation (CSV Driven)

  Background:
    Given user opens Myntra website for categories

  Scenario Outline: Validate category navigation - <test_name>
    When user hovers Home & Living menu for categories
    And user selects category "<category>"
    Then page URL should contain "<expected_url>"
    And if sort option exists "<sort_option>" apply
    And if brand exists "<brand>" apply brand filter

    Examples:
      | test_name            | category             | expected_url         | sort_option        | brand |
      | table_lamps          | Table Lamps          | tablelamp            |                    |       |
      | cups_mugs            | Cups and Mugs        | cups-and-mugs        | Price: High to Low |       |
      | door_mats            | Door Mats            | doormats             |                    | Aura  |
      | bathroom_accessories | Bathroom Accessories | bathroom-accessories | Popularity         |       |

  Scenario: Negative - Invalid sort option must not exist on Bedsheets page
    When user hovers Home & Living menu for categories
    And user selects category "Bedsheets"
    Then page URL should contain "bedsheets"
    And invalid sort option should not exist

  Scenario: Negative - Invalid filters must not exist on Organisers page
    When user hovers Home & Living menu for categories
    And user selects category "Organisers"
    Then page URL should contain "organisers"
    And invalid filters should not exist