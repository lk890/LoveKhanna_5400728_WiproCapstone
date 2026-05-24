Feature: Myntra Home & Living E2E Shopping Flow

  Scenario: User buys Aromas & Candles product successfully

    Given user opens Myntra website
    Then page title should contain "Myntra"

    When user hovers on Home & Living menu
    And user selects "Aromas & Candles" category

    Then category page URL should contain aroma or candles or fragrance
    And category heading should be valid

    When user selects first product
    And user switches to product tab

    Then Add to Bag button should be visible
    When user adds product to bag

    Then cart count should update
    When user opens shopping bag

    Then product should be present in cart

    When user clicks PLACE ORDER

    Then user should be redirected to login or checkout page

    When user enters mobile number "9760076422"
    And user completes OTP manually

    Then user should land on checkout cart page

    When user opens final cart page
    Then cart should contain at least one product